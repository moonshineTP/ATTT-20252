# Build báo cáo PKI → report/main.pdf
# Chạy trong PowerShell:
#   Set-Location "D:\LapTrinh\System\ATTT-20252"
#   .\scripts\build_report.ps1

$ErrorActionPreference = "Continue"
$MiKTeX = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64"
$pdflatex = Join-Path $MiKTeX "pdflatex.exe"
$biber = Join-Path $MiKTeX "biber.exe"

if (-not (Test-Path $pdflatex)) {
    Write-Error "Không tìm thấy pdflatex tại $pdflatex. Cài MiKTeX hoặc sửa đường dẫn trong script này."
    exit 1
}

$report = Join-Path $PSScriptRoot "..\report" | Resolve-Path
Set-Location $report

$args = @("-synctex=1", "-interaction=nonstopmode", "-file-line-error", "main.tex")

Write-Host "=== pdflatex (1/3) ==="
& $pdflatex @args
Write-Host "=== biber ==="
if (Test-Path $biber) { & $biber main } else { Write-Warning "biber not found" }
Write-Host "=== pdflatex (2/3) ==="
& $pdflatex @args
Write-Host "=== pdflatex (3/3) ==="
& $pdflatex @args

$pdf = Join-Path $report "main.pdf"
if (Test-Path $pdf) {
    Write-Host "`nOK: $pdf ($((Get-Item $pdf).Length) bytes)"
} else {
    Write-Host "`nBuild thất bại. Mở report/main.log và tìm dòng bắt đầu bằng '!'."
    Write-Host "Nếu thiếu gói MiKTeX: mở MiKTeX Console → Updates → Check for updates → Update now"
    Write-Host "Sau đó: Packages → cài csquotes, babel-vietnamese, vntex, biblatex, biber, tcolorbox, tikz..."
    exit 1
}
