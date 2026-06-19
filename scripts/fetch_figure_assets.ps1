# Tải ảnh Wikimedia vào report/assets (330px, tránh rate limit).
#   cd "D:\LapTrinh\System\ATTT-20252"
#   .\scripts\fetch_figure_assets.ps1

$ErrorActionPreference = "Stop"
$assets = Join-Path $PSScriptRoot "..\report\assets" | Resolve-Path
$ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ATTT-PKI-Report/1.0"

$files = [ordered]@{
    "mitm_attack.png" = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Man_in_the_middle_attack.svg/330px-Man_in_the_middle_attack.svg.png"
    "pki_hierarchy.png" = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Public_key_infrastructure.svg/330px-Public_key_infrastructure.svg.png"
    "x509_structure.png" = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/X.509.svg/330px-X.509.svg.png"
    "tls_handshake.png" = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/SSL_handshake_with_only_one_certificate.svg/330px-SSL_handshake_with_only_one_certificate.svg.png"
    "certificate_transparency.png" = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Certificate_Transparency.svg/330px-Certificate_Transparency.svg.png"
    "openssl_logo.png" = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/OpenSSL_logo.svg/330px-OpenSSL_logo.svg.png"
    "letsencrypt_logo.png" = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Lets_Encrypt_logo.svg/330px-Lets_Encrypt_logo.svg.png"
}

Write-Host "Target: $assets"
Write-Host "Chi tiet link: report/assets/DOWNLOAD_LINKS.md"
$i = 0
foreach ($name in $files.Keys) {
    if ($i -gt 0) {
        Write-Host "Doi 15 giay..."
        Start-Sleep -Seconds 15
    }
    $dest = Join-Path $assets $name
    if ((Test-Path $dest) -and (Get-Item $dest).Length -gt 5000) {
        Write-Host "Skip $name (da co)"
        $i++
        continue
    }
    Write-Host "Downloading $name ..."
    try {
        Invoke-WebRequest -Uri $files[$name] -OutFile $dest -UserAgent $ua
        Write-Host "  OK  $((Get-Item $dest).Length) bytes"
    } catch {
        Write-Warning "  FAIL $name : $($_.Exception.Message)"
        Write-Host "  -> Tai tay: report/assets/DOWNLOAD_LINKS.md"
    }
    $i++
}
Write-Host "Done."
