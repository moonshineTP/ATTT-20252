"""
fetch_figure_assets.py
----------------------
Tải các hình minh họa PKI từ nguồn mở (Wikimedia Commons) vào report/assets/.
Chạy lại script này nếu cần khôi phục tệp hình.

Usage:
    .venv\\Scripts\\python.exe scripts\\fetch_figure_assets.py
"""

from __future__ import annotations

import pathlib
import time
import urllib.request

BASE_DIR = pathlib.Path(__file__).parent.parent
ASSETS = BASE_DIR / "report" / "assets"

# Use standard Wikimedia thumbnail widths (see https://w.wiki/GHai).
DOWNLOADS: dict[str, str] = {
    "mitm_attack.png": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "e/e3/Man_in_the_middle_attack.svg/640px-Man_in_the_middle_attack.svg.png"
    ),
    "tls_handshake.png": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "1/19/SSL_handshake_with_only_one_certificate.svg/"
        "640px-SSL_handshake_with_only_one_certificate.svg.png"
    ),
    "x509_structure.png": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "5/5a/X.509.svg/640px-X.509.svg.png"
    ),
    "pki_hierarchy.png": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "5/5f/Public_key_infrastructure.svg/640px-Public_key_infrastructure.svg.png"
    ),
    "certificate_transparency.png": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "a/a6/Certificate_Transparency.svg/640px-Certificate_Transparency.svg.png"
    ),
    "openssl_logo.png": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "3/3b/OpenSSL_logo.svg/320px-OpenSSL_logo.svg.png"
    ),
    "letsencrypt_logo.png": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/"
        "4/4e/Lets_Encrypt_logo.svg/320px-Lets_Encrypt_logo.svg.png"
    ),
}


def fetch(url: str, dest: pathlib.Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ATTT-PKI-Report/1.0 (academic; manual fetch)"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())
    print(f"  OK  {dest.name} ({dest.stat().st_size:,} bytes)")


def main() -> None:
    print(f"Target: {ASSETS}")
    print("Waiting 3s between downloads to respect Wikimedia rate limits...")
    for i, (name, url) in enumerate(DOWNLOADS.items()):
        if i:
            time.sleep(3)
        fetch(url, ASSETS / name)
    print("Done. See report/assets/SOURCES.md for attribution.")


if __name__ == "__main__":
    main()
