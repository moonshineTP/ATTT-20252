# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.


## Administrative objective

This repository is the organizatioon for a Vietnamese course report on Public Key Infrastructure (PKI)
for the course "Nhập môn An toàn thông tin" at HUST/SOICT. Future work should preserve the report
as a camera-ready academic artifact: consistent Vietnamese terminology, supported technical claims,
complete references, stable LaTeX compilation, and no scratch or process notes in the final report text.


## Execution environment

Use the checked-in Windows virtual environment for Python work. Do not use bare `python` or `python3` unless the user explicitly asks for a different interpreter.

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

The project path contains spaces and Vietnamese characters. If Python output fails with Windows encoding errors,
run the command from PowerShell/cmd after enabling UTF-8 output:

```bat
chcp 65001
set PYTHONIOENCODING=utf-8
.venv\Scripts\python.exe scripts\wordcount.py
```


## Common commands

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

If `latexmk` is available:

```powershell
cd report
latexmk -synctex=1 -interaction=nonstopmode -file-line-error -pdf main.tex
```


## Crucial skills

### Report LaTeX skill

For work under `report/`, apply `.claude/skills/latex-tips-and-tricks/SKILL.md`.
Keep `.tex` source readable with semantic line breaks and delete stale commented-out prose.
Use structural LaTeX commands rather than manual visual formatting.
Every figure, table, equation, and section reference should use stable labels with prefixes such as `fig:`, `tab:`, `eq:`, and `sec:`.
Use `biblatex`/`biber` through `report/references.bib`; add supported claims as citations, not bare URLs.
Prefer `booktabs` tables, captions below figures and above tables, and cite floats before they appear.
Treat LaTeX warnings, broken references, missing captions, and overfull boxes as report-quality defects.
After editing any file under `report/`, run Windows `pdflatex` before ending the pass:

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

The CLI package is installed from `git+https://github.com/oriolrius/pki-manager-cli.git` and is recorded in `requirements.txt`.
Do not use a global `pki` command unless the user explicitly asks for a different environment.

PKI Manager credentials must live outside the repository and outside any skill folder.
Use `~/.config/pki-cli/.env` for live credentials.
A non-secret template may exist at `~/.config/pki-cli/.env.template`.
The required variables are `PKI_API_URL`, `PKI_OIDC_URL`, `PKI_CLIENT_ID`, and `PKI_CLIENT_SECRET`;
`PKI_API_URL` must end with `/api/v1`.

### Windows/WSL coordination

This project is on the Windows filesystem and is operated from WSL. Do not assume Windows and WSL share PATH. When calling Windows GitHub CLI from WSL PowerShell, reload PATH first:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
gh --version
```

Windows GitHub CLI is installed at `C:\Program Files\GitHub CLI\gh.exe`, visible in WSL as `/mnt/c/Program Files/GitHub CLI/gh.exe`.


## Architecture

`report/main.tex` is the report entry point. It defines document formatting, packages, bibliography setup, PDF metadata, title page inclusion, chapter order, lists, and final bibliography rendering. Treat it as the orchestration file rather than chapter prose.

`report/chapter/` contains the camera-ready LaTeX chapter files. The intended chapter flow is: introduction, public-key cryptography foundations, PKI architecture, X.509 and standards, real deployments, open-source PKI systems, challenges and trends, then conclusion.

`report/references.bib` is the bibliography source for `biblatex` with `biber` and IEEE-style numeric citations. When adding claims in the report, prefer adding or reusing BibTeX entries rather than leaving bare URLs in prose.

`report/assets/` contains figures used by the report. Keep Vietnamese captions in report context and check generated/exported images for cropping, broken diacritics, and unreadable labels.

`report/specs/` contains the source-of-truth planning notes for requirements, outline, terminology, and source material summaries. Use these notes to preserve scope and terminology, especially `00_yeu_cau_bao_cao.md`, `06_outline_bao_cao.md`, and `07_tu_vung.md`.

`material/` contains source PDFs from course material. `scripts/extract_pdfs.py` reads those PDFs, and `scripts/material_summary.py` filters extracted text for PKI-relevant passages. The raw extracted text under `scripts/raw/` is supporting material, not final prose.


## Report scope and terminology

The report must cover five required areas from the assignment:
PKI structure, digital certificates and standards, real deployment and transaction applications,
open-source PKI systems, and future aspects.

Use Vietnamese as the primary report language. Preserve established terminology from `report/specs/07_tu_vung.md`.
Further Vietnamese dictation can be refer in `.claude/skills/antipattern-text-vi` for consistent phrasing and diacritics.

For polished report edits, remove placeholders, TODOs, unsupported claims, and internal commentary.
Do not leave console-scope or memory-scope convention in the final report text.
The report should read as a standalone academic artifact, which can stand on its own.
