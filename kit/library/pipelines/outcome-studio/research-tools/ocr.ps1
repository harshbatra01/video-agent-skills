# Windows built-in OCR (Windows.Media.Ocr) over a list of images.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File ocr.ps1 <listfile> <out.jsonl>
# listfile: one absolute image path per line. Output: one JSON line per image:
# {"path":..., "w":..., "h":..., "lines":[{"text":..., "x":..,"y":..,"w":..,"h":..,"words":n}, ...]}
param([string]$ListFile, [string]$OutFile)
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.SoftwareBitmap, Windows.Graphics, ContentType = WindowsRuntime]
$null = [Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime]
$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($WinRtTask, $ResultType) {
    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
    $netTask = $asTask.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$paths = Get-Content -LiteralPath $ListFile -Encoding UTF8 | Where-Object { $_.Trim() -ne '' }
$sw = New-Object System.IO.StreamWriter($OutFile, $true, (New-Object System.Text.UTF8Encoding($false)))
foreach ($p0 in $paths) {
    $p = [string]$p0
    try {
        $file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($p)) ([Windows.Storage.StorageFile])
        $stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
        $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
        $bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
        $res = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
        $lines = @()
        foreach ($ln in $res.Lines) {
            $xs = @(); $ys = @(); $xe = @(); $ye = @()
            foreach ($wd in $ln.Words) { $r = $wd.BoundingRect; $xs += $r.X; $ys += $r.Y; $xe += ($r.X + $r.Width); $ye += ($r.Y + $r.Height) }
            $x0 = ($xs | Measure-Object -Minimum).Minimum; $y0 = ($ys | Measure-Object -Minimum).Minimum
            $x1 = ($xe | Measure-Object -Maximum).Maximum; $y1 = ($ye | Measure-Object -Maximum).Maximum
            $lines += [ordered]@{ text = $ln.Text; x = [int]$x0; y = [int]$y0; w = [int]($x1 - $x0); h = [int]($y1 - $y0); words = $ln.Words.Count }
        }
        $obj = [ordered]@{ path = $p; w = $bitmap.PixelWidth; h = $bitmap.PixelHeight; lines = $lines }
        $sw.WriteLine(($obj | ConvertTo-Json -Compress -Depth 5))
        $stream.Dispose()
    } catch {
        $sw.WriteLine((@{ path = $p; err = $_.Exception.Message } | ConvertTo-Json -Compress))
    }
}
$sw.Close()
Write-Output ("done " + $paths.Count)
