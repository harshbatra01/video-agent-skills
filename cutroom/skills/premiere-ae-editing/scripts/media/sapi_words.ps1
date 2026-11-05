# Word-level timings with Windows desktop speech recognition (System.Speech dictation), absolute stream times.
# usage: powershell -File sapi_words.ps1 in.wav out.tsv   (tsv: start  duration  word  confidence)
param([string]$wav, [string]$out)
Add-Type -AssemblyName System.Speech
$info = [System.Speech.Recognition.SpeechRecognitionEngine]::InstalledRecognizers() | Where-Object { $_.Culture.Name -like 'en-*' } | Select-Object -First 1
$eng = New-Object System.Speech.Recognition.SpeechRecognitionEngine($info)
$eng.LoadGrammar((New-Object System.Speech.Recognition.DictationGrammar))
$eng.SetInputToWaveFile($wav)
$eng.EndSilenceTimeout = [TimeSpan]::FromSeconds(0.25)
$results = New-Object System.Collections.ArrayList
$null = Register-ObjectEvent -InputObject $eng -EventName SpeechRecognized -SourceIdentifier SR -MessageData $results -Action { [void]$Event.MessageData.Add($EventArgs.Result) }
$null = Register-ObjectEvent -InputObject $eng -EventName RecognizeCompleted -SourceIdentifier RC
$eng.RecognizeAsync([System.Speech.Recognition.RecognizeMode]::Multiple)
$null = Wait-Event -SourceIdentifier RC -Timeout 900
Start-Sleep -Milliseconds 300
$lines = @()
foreach ($r in $results) {
    $ph = $r.Audio.AudioPosition.TotalSeconds
    $lines += ("# {0:N3} {1:N3} {2}" -f $ph, $r.Audio.Duration.TotalSeconds, $r.Text)
    foreach ($w in $r.Words) {
        try {
            $a = $r.GetAudioForWordRange($w, $w)
            $lines += ("{0:N3}`t{1:N3}`t{2}`t{3:N2}" -f ($ph + $a.AudioPosition.TotalSeconds), $a.Duration.TotalSeconds, $w.Text, $w.Confidence)
        } catch { $lines += ("?`t?`t{0}`t{1:N2}" -f $w.Text, $w.Confidence) }
    }
}
$lines | Out-File $out -Encoding utf8
Unregister-Event -SourceIdentifier SR; Unregister-Event -SourceIdentifier RC
