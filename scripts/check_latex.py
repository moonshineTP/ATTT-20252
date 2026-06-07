"""
check_latex.py
--------------
Kiểm tra các vấn đề phổ biến trong file .tex trước khi nộp:
  1. \ref{} và \cite{} chưa được define (labels/keys không tồn tại)
  2. \label{} bị duplicate
  3. TODO / FIXME / PLACEHOLDER còn sót lại
  4. Figures/tables không có caption hoặc label

Usage:
    python script/check_latex.py
    python script/check_latex.py chapters/chap3.tex
"""

import re
import sys
import pathlib
from collections import defaultdict

BASE_DIR = pathlib.Path(__file__).parent.parent


def collect_all_tex(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(root.rglob('*.tex'))


def parse_file(path: pathlib.Path) -> dict:
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except FileNotFoundError:
        return {}

    # Remove comments
    text_no_comments = re.sub(r'%.*', '', text)

    labels   = re.findall(r'\\label\{([^}]+)\}', text_no_comments)
    refs     = re.findall(r'\\(?:ref|eqref|pageref|autoref|nameref)\{([^}]+)\}', text_no_comments)
    cites    = re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', text_no_comments)
    todos    = [(m.start(), m.group()) for m in re.finditer(
                    r'(?i)(TODO|FIXME|PLACEHOLDER|XX+|FILL[_ ]IN)', text_no_comments)]

    # Detect figures/tables missing \caption or \label
    env_issues = []
    for env in ('figure', 'table'):
        for m in re.finditer(rf'\\begin\{{{env}\*?\}}(.*?)\\end\{{{env}\*?\}}',
                             text_no_comments, re.DOTALL):
            block = m.group(1)
            if '\\caption' not in block:
                lineno = text[:m.start()].count('\n') + 1
                env_issues.append(f"  Line ~{lineno}: \\begin{{{env}}} missing \\caption")
            if '\\label' not in block:
                lineno = text[:m.start()].count('\n') + 1
                env_issues.append(f"  Line ~{lineno}: \\begin{{{env}}} missing \\label")

    # Expand comma-separated cite keys
    all_cite_keys = []
    for c in cites:
        all_cite_keys.extend(k.strip() for k in c.split(','))

    return {
        'labels': labels,
        'refs': refs,
        'cites': all_cite_keys,
        'todos': todos,
        'env_issues': env_issues,
        'raw': text_no_comments,
    }


def main():
    if len(sys.argv) > 1:
        files = [BASE_DIR / sys.argv[1]]
    else:
        files = collect_all_tex(BASE_DIR)

    if not files:
        print("No .tex files found.")
        return

    all_labels: dict[str, list[str]] = defaultdict(list)  # label -> [files]
    all_refs:   set[str] = set()
    all_cites:  set[str] = set()
    bib_keys:   set[str] = set()
    issues: list[str] = []

    # Collect defined bib keys from .bib files
    for bib in BASE_DIR.rglob('*.bib'):
        content = bib.read_text(encoding='utf-8', errors='ignore')
        for m in re.finditer(r'@\w+\{([^,\s]+)', content):
            bib_keys.add(m.group(1).strip())

    for fpath in files:
        data = parse_file(fpath)
        if not data:
            continue
        rel = fpath.relative_to(BASE_DIR)

        for lbl in data.get('labels', []):
            all_labels[lbl].append(str(rel))

        for ref in data.get('refs', []):
            all_refs.add(ref)

        for cite in data.get('cites', []):
            all_cites.add(cite)

        for _, todo_text in data.get('todos', []):
            issues.append(f"[TODO]  {rel}: '{todo_text}'")

        for env_issue in data.get('env_issues', []):
            issues.append(f"[ENV]   {rel}: {env_issue}")

    # Check for duplicate labels
    for lbl, lbl_files in all_labels.items():
        if len(lbl_files) > 1:
            issues.append(f"[DUPE]  \\label{{{lbl}}} defined in: {', '.join(lbl_files)}")

    # Check for undefined \ref targets
    defined_labels = set(all_labels.keys())
    for ref in sorted(all_refs):
        if ref not in defined_labels:
            issues.append(f"[REF?]  \\ref{{{ref}}} — label not defined in any .tex file")

    # Check for undefined \cite keys
    if bib_keys:
        for cite in sorted(all_cites):
            if cite not in bib_keys:
                issues.append(f"[CITE?] \\cite{{{cite}}} — key not found in any .bib file")
    else:
        issues.append("[INFO]  No .bib files found — cite keys not validated")

    # Report
    print("=" * 60)
    print("LaTeX Check Report")
    print("=" * 60)
    if not issues:
        print("No issues found! Ready to compile.")
    else:
        for issue in issues:
            print(issue)
        print(f"\nTotal: {len(issues)} issue(s) found.")

    print(f"\nStats: {len(defined_labels)} labels, {len(all_refs)} \\refs, "
          f"{len(all_cites)} \\cites, {len(bib_keys)} bib keys")


if __name__ == '__main__':
    main()
