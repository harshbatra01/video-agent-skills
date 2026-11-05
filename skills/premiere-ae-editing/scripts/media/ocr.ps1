# Windows built-in OCR (Windows.Media.Ocr): word boxes for each image. usage: powershell -File ocr.ps1 out.json img1 img2 ...
param([string]$out, [Parameter(ValueFromRemainingArguments = $true)][string[]]$images)
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($op, [Type]$t) { $m = $asTask.MakeGenericMethod($t); $task = $m.Invoke($null, @($op)); $task.Wait(-1) | Out-Null; $task.Result }
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$all = @{}
foreach ($img in $images) {
    $file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($img)) ([Windows.Storage.StorageFile])
    $stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $dec = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bmp = Await ($dec.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    # OCR engine has a max image dimension; scale down if needed
    $max = [Windows.Media.Ocr.OcrEngine]::MaxImageDimension
    $scale = 1.0
    if ($bmp.PixelWidth -gt $max -or $bmp.PixelHeight -gt $max) {
        $scale = [Math]::Min($max / $bmp.PixelWidth, $max / $bmp.PixelHeight)
        $tr = New-Object Windows.Graphics.Imaging.BitmapTransform
        $tr.ScaledWidth = [uint32]($bmp.PixelWidth * $scale); $tr.ScaledHeight = [uint32]($bmp.PixelHeight * $scale)
        $bmp = Await ($dec.GetSoftwareBitmapAsync([Windows.Graphics.Imaging.BitmapPixelFormat]::Bgra8, [Windows.Graphics.Imaging.BitmapAlphaMode]::Premultiplied, $tr, [Windows.Graphics.Imaging.ExifOrientationMode]::IgnoreExifOrientation, [Windows.Graphics.Imaging.ColorManagementMode]::DoNotColorManage)) ([Windows.Graphics.Imaging.SoftwareBitmap])
    }
    $res = Await ($engine.RecognizeAsync($bmp)) ([Windows.Media.Ocr.OcrResult])
    $lines = @()
    foreach ($ln in $res.Lines) {
        $ws = @()
        foreach ($w in $ln.Words) { $r = $w.BoundingRect; $ws += , @($w.Text, [Math]::Round($r.X / $scale, 1), [Math]::Round($r.Y / $scale, 1), [Math]::Round($r.Width / $scale, 1), [Math]::Round($r.Height / $scale, 1)) }
        $lines += , @{ text = $ln.Text; words = $ws }
    }
    $all[[System.IO.Path]::GetFileName($img)] = $lines
    $stream.Dispose()
}
$all | ConvertTo-Json -Depth 6 -Compress | Out-File $out -Encoding utf8
