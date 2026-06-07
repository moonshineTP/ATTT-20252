"""
wordcount.py
------------
Đếm số từ xấp xỉ trong các file .tex của báo cáo.
Loại bỏ LaTeX commands, comments, và math environments trước khi đếm.

Usage:
    python script/wordcount.py
    python script/wordcount.py chapters/chap3.tex   # đếm một file cụ thể
"""

import re
import sys
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent


def strip_latex(text: str) -> str:
    """Remove LaTeX markup, leaving prose words only."""
    # Remove comments
    text = re.sub(r'%.*', '', text)
    # Remove display math  \[ ... \]  and  $$ ... $$
    text = re.sub(r'\$\$.*?\$\$', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\\\[.*?\\\]', ' ', text, flags=re.DOTALL)
    # Remove inline math $ ... $
    text = re.sub(r'\$[^$]*?\$', ' ', text)
    # Remove \begin{...}...\end{...} blocks (figure, table, equation, etc.)
    text = re.sub(r'\\begin\{[^}]+\}.*?\\end\{[^}]+\}', ' ', text, flags=re.DOTALL)
    # Remove common LaTeX commands with their arguments: \command{arg}
    text = re.sub(r'\\[a-zA-Z]+\*?\{[^{}]*\}', ' ', text)
    # Remove remaining LaTeX commands (no args): \command
    text = re.sub(r'\\[a-zA-Z]+\*?', ' ', text)
    # Remove leftover braces
    text = re.sub(r'[{}]', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def count_words_in_file(tex_path: pathlib.Path) -> int:
    try:
        text = tex_path.read_text(encoding='utf-8', errors='ignore')
    except FileNotFoundError:
        print(f"  [NOT FOUND] {tex_path}")
        return 0
    clean = strip_latex(text)
    words = [w for w in clean.split() if re.search(r'[a-zA-ZÀ-ỹ]', w)]
    return len(words)


def main():
    if len(sys.argv) > 1:
        # Count a specific file
        target = pathlib.Path(sys.argv[1])
        if not target.is_absolute():
            target = BASE_DIR / target
        count = count_words_in_file(target)
        print(f"{target.name}: {count:,} words")
        return

    # Auto-discover all .tex files
    tex_files = sorted(BASE_DIR.rglob('*.tex'))
    if not tex_files:
        print("No .tex files found.")
        return

    total = 0
    print(f"{'File':<45} {'Words':>8}")
    print("-" * 55)
    for f in tex_files:
        rel = f.relative_to(BASE_DIR)
        count = count_words_in_file(f)
        total += count
        status = " ✓" if count > 100 else " (empty/stub)"
        print(f"{str(rel):<45} {count:>8,}{status}")

    print("-" * 55)
    print(f"{'TOTAL':<45} {total:>8,}")
    target_words = 5000
    pct = total / target_words * 100
    print(f"\nTarget: {target_words:,} words  →  {pct:.0f}% completed")
    if total < target_words:
        print(f"Still need ~{target_words - total:,} more words.")
    else:
        print("Target reached!")


if __name__ == '__main__':
    main()
