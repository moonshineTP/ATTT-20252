"""
extract_pdfs.py
---------------
Extract text from all PDF files in the material/ folder and save raw text
to script/raw/ for inspection before summarizing.
"""

import pdfplumber
import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
MATERIAL_DIR = BASE_DIR / "material"
RAW_DIR = pathlib.Path(__file__).parent / "raw"
RAW_DIR.mkdir(exist_ok=True)

PDF_FILES = ["requirements.pdf", "chap1.pdf", "chap2.pdf", "chap3.pdf", "chap4.pdf"]

for pdf_name in PDF_FILES:
    pdf_path = MATERIAL_DIR / pdf_name
    if not pdf_path.exists():
        print(f"[SKIP] {pdf_name} not found")
        continue

    out_path = RAW_DIR / (pdf_name.replace(".pdf", ".txt"))
    text_pages = []

    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        print(f"[READ] {pdf_name} — {total} pages")
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text() or ""
            text_pages.append(f"--- Page {i+1} ---\n{page_text}")

    full_text = "\n\n".join(text_pages)
    out_path.write_text(full_text, encoding="utf-8")
    print(f"  -> Saved {len(full_text)} chars to {out_path.name}")

print("\nDone! Raw text is in script/raw/")
