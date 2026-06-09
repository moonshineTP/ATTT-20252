"""
material_summary.py
-------------------
Tổng hợp nội dung từ script/raw/*.txt (các file đã extract từ PDF giáo trình)
và lọc những đoạn liên quan đến PKI, X.509, chứng chỉ số, chữ ký số.

Output: script/raw/pki_relevant_passages.txt — dùng làm nguồn tham khảo
        khi viết báo cáo, tránh phải đọc lại toàn bộ PDF.

Usage:
    python script/material_summary.py
"""

import re
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
RAW_DIR  = pathlib.Path(__file__).parent / 'raw'
OUT_FILE = RAW_DIR / 'pki_relevant_passages.txt'

# Từ khóa liên quan đến PKI và các chủ đề của báo cáo
PKI_KEYWORDS = [
    # PKI core
    r'\bPKI\b', r'public key infrastructure', r'hạ tầng khóa',
    r'certificate authority', r'\bCA\b', r'chứng chỉ số', r'digital certificate',
    r'X\.509', r'x509',
    # Crypto
    r'asymmetric', r'bất đối xứng', r'khóa công khai', r'public key',
    r'private key', r'khóa bí mật', r'RSA', r'ECC', r'elliptic curve',
    r'digital signature', r'chữ ký số',
    r'hash function', r'hàm băm', r'SHA', r'MD5',
    # Trust
    r'chain of trust', r'root CA', r'intermediate CA',
    r'certificate chain', r'trust store', r'trust anchor',
    # Revocation
    r'revocation', r'thu hồi', r'CRL', r'OCSP', r'stapling',
    # Protocols
    r'\bTLS\b', r'\bSSL\b', r'\bHTTPS\b', r'handshake',
    # Attacks
    r'MITM', r'man.in.the.middle', r'DigiNotar', r'Symantec',
    # Modern
    r'certificate transparency', r'\bCT\b log', r'Let.s Encrypt',
    r'ACME', r'post.quantum', r'DID\b',
]

COMPILED = [re.compile(kw, re.IGNORECASE) for kw in PKI_KEYWORDS]


def is_relevant(text: str) -> bool:
    return any(pat.search(text) for pat in COMPILED)


def extract_relevant_passages(raw_text: str, source_name: str) -> list[str]:
    """Split by page, then by paragraph. Return relevant paragraphs."""
    passages = []
    pages = raw_text.split('--- Page ')
    for page_block in pages[1:]:  # skip header before first page
        page_num_match = re.match(r'(\d+)', page_block)
        page_num = page_num_match.group(1) if page_num_match else '?'
        content = page_block[page_block.find('\n'):].strip()

        # Split into paragraphs (double newline or single newline runs)
        paragraphs = re.split(r'\n{2,}', content)
        for para in paragraphs:
            para = para.strip()
            if len(para) < 30:  # skip very short fragments
                continue
            if is_relevant(para):
                passages.append(f"[{source_name} p.{page_num}]\n{para}")
    return passages


def main():
    raw_files = sorted(RAW_DIR.glob('*.txt'))
    if not raw_files:
        print("No raw text files found. Run extract_pdfs.py first.")
        return

    all_passages = []
    stats = {}

    for raw_file in raw_files:
        if raw_file.name == OUT_FILE.name:
            continue  # skip own output
        text = raw_file.read_text(encoding='utf-8', errors='ignore')
        passages = extract_relevant_passages(text, raw_file.stem)
        stats[raw_file.name] = len(passages)
        all_passages.extend(passages)
        print(f"  {raw_file.name}: {len(passages)} relevant passages found")

    separator = '\n' + '=' * 70 + '\n'
    output = separator.join(all_passages)
    OUT_FILE.write_text(output, encoding='utf-8')

    print(f"\nTotal: {len(all_passages)} passages → saved to {OUT_FILE.name}")
    print("\nUse this file as quick-reference when writing chapters in main.tex.")


if __name__ == '__main__':
    main()
