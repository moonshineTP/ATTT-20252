# CLAUDE.md

This file provides administrative guidance to Claude Code when working in this repository.


## Objective

This repository is the organization for a Vietnamese curriculum course report
with the topic of Public Key Infrastructure (PKI) for the course "Nhập môn An toàn thông tin".
Additionally, a demonstration of miniature PKI - client authorization session is implemented,
attached with a dedicated short technical report.


## Execution environment

Use the checked-in Windows virtual environment for Python work.
Do not use bare `python` or `python3`.

From PowerShell:

```powershell
.\.venv\Scripts\python.exe scripts\check_latex.py
.\.venv\Scripts\python.exe scripts\wordcount.py
```

From cmd.exe:

```bat
.venv\Scripts\python.exe scripts\check_latex.py
.venv\Scripts\python.exe scripts\wordcount.py
```

From WSL/bash in this workspace:

```bash
./.venv/Scripts/python.exe scripts/check_latex.py
./.venv/Scripts/python.exe scripts/wordcount.py
```

The project path contains spaces and Vietnamese characters.
If Python output fails with Windows encoding errors, enabling UTF-8 output:

```bat
chcp 65001
set PYTHONIOENCODING=utf-8
.venv\Scripts\python.exe scripts\wordcount.py
```


## Common commands

### Report workflow

Validate LaTeX labels, citations, TODO markers, and figure/table caption/label coverage:

```powershell
.\.venv\Scripts\python.exe scripts\check_latex.py
.\.venv\Scripts\python.exe scripts\check_latex.py report\chapter\chap3.tex
```

Count report words:

```powershell
.\.venv\Scripts\python.exe scripts\wordcount.py
.\.venv\Scripts\python.exe scripts\wordcount.py report\chapter\chap3.tex
```

Extract text from source PDFs in `material/` into `scripts/raw/`:

```powershell
.\.venv\Scripts\python.exe scripts\extract_pdfs.py
```

Regenerate PKI-relevant extracted passages:

```powershell
.\.venv\Scripts\python.exe scripts\material_summary.py
```

Build the report PDF with the same sequence configured in `.vscode/settings.json`:

```powershell
cd report
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
biber main
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
```

### Demo workflow 


## Crucial skills

### Writing skill

- Do not over-adhere to console instructions.
- Do not repeat structure on multiple sections/subsections.
- Do not use the "\textbf{Point:} description" prose. Prefer direct description.

### Report LaTeX skill

- For work under `report/`, fetch `.claude/skills/latex-tips-and-tricks/SKILL.md` on fresh session.
- Keep `.tex` source readable with semantic line breaks and delete stale commented-out prose.
- Use structural LaTeX commands rather than manual layout alignments.
- Every figure, table, equation, and section reference should use stable labels with prefixes such as `fig:`, `tab:`, `eq:`, and `sec:`.
- Use `biblatex`/`biber` through `report/references.bib`; add supported claims as citations via natbib.
- Prefer `booktabs` tables, captions below figures and above tables, and cite floats before they appear.
- Treat LaTeX warnings, broken references, missing captions, and overfull boxes as report-quality defects.
- Do not read the entire LaTeX log for build-quality checks. Inspect targeted excerpts or filtered warnings/errors only.
- Run Windows `pdflatex` build before finishing the pass

```powershell
cd report
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
```

### PKI Manager skill

A project-level Claude Code skill is installed at `.claude/skills/pki-cli`. Use it for PKI Manager
operations such as CA management, certificate issuance, renewal, revocation, download, CRL management,
and X.509 certificate inspection.

Run the PKI Manager CLI through the native command installed in the project virtualenv:

```bash
./.venv/Scripts/pki.exe --help
./.venv/Scripts/pki.exe config
```

The CLI package is installed from `git+https://github.com/oriolrius/pki-manager-cli.git` and is recorded in `requirements.txt`. If this is not installed or configured yet, inform the user.


### Windows/WSL coordination

One colleague's machine use the Windows filesystem and is operated from WSL.
Do not assume Windows and WSL share PATH.
When calling Windows GitHub CLI from WSL PowerShell, reload PATH first:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
gh --version
```


## Architecture

`report/main.tex` is the report entry point. Treat it as the orchestration file.

`report/chapter/` contains the camera-ready LaTeX chapter files. The intended chapter flow is: introduction, public-key cryptography foundations, PKI architecture, X.509 and standards, real deployments, open-source PKI systems, challenges and trends, then conclusion.

`report/references.bib` is the bibliography source for `biblatex` with `biber` and IEEE-style numeric citations.

`report/assets/` contains figures used by the report.

`report/specs/` contains the source-of-truth planning notes for requirements, outline, terminology, and source material summaries. Use these notes to preserve scope and terminology, especially `00_yeu_cau_bao_cao.md`, `06_outline_bao_cao.md`, and `07_tu_vung.md`.

`material/` contains source PDFs from course material. `scripts/extract_pdfs.py` reads those PDFs, and `scripts/material_summary.py` filters extracted text for PKI-relevant passages.


## Report scope and terminology

The report must cover five required areas from the assignment:
PKI structure, digital certificates and standards, real deployment and transaction applications,
open-source PKI systems, and future aspects.

Use Vietnamese as the primary report language.
Preserve established terminology from `report/specs/07_tu_vung.md`.
Refer `.claude/skills/antipattern-text-vi` for combating AI prose in Vietnamese texts.

For polished report edits, remove placeholders, TODOs, unsupported claims, and internal commentary.
Do not leave console-scope or memory-scope convention in the final report text.
The report should read as a standalone academic artifact, which can stand on its own.
