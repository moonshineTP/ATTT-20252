# ATTT PKI Report & Demo

## Objective
This repository hosts a Vietnamese curriculum course report on **Public Key Infrastructure (PKI)** for the course "Nhập môn An toàn thông tin" at HUST/SOICT.

Alongside the theoretical research, this project also features a **miniature PKI demonstration** (client authorization session) attached with a dedicated technical report. The goal is to bridge the gap between cryptographic theory, X.509 standards, and real-world PKI implementation mechanics.

## Repository Structure
- `report/`: The core LaTeX document source files.
  - `main.tex`: The entry orchestration file.
  - `chapter/`: Contains the camera-ready LaTeX chapters (foundations, architecture, X.509, deployments, challenges).
  - `references.bib`: Bibliography source for IEEE-style numeric citations.
  - `specs/`: Source-of-truth planning notes for requirements, outline, and terminology.
- `material/`: Source PDFs and reference materials from the course.
- `scripts/`: Python utility scripts for data extraction, summarization, and LaTeX validation.
- `.venv/`: The checked-in Windows virtual environment for executing Python scripts and the PKI Manager CLI.

## Common Commands

All Python operations must be executed using the checked-in virtual environment (`.venv`) to ensure reproducibility.

### Report Workflow

**1. Validate Document Health**
Check for missing LaTeX labels, citations, TODO markers, and figure/table coverage:
```powershell
.\.venv\Scripts\python.exe scripts\check_latex.py
```

**2. Count Words**
```powershell
.\.venv\Scripts\python.exe scripts\wordcount.py
```

**3. Build the PDF Report**
Navigate to the `report` directory and execute the standard `pdflatex` build sequence:
```powershell
cd report
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
biber main
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
```

*(Alternatively, use `latexmk -pdf main.tex` if available).*

### Demo Workflow (PKI Manager)

A project-level CLI is installed to operate the PKI Manager (CA management, certificate issuance, renewal, revocation, and inspection).

```bash
# Check CLI capabilities
./.venv/Scripts/pki.exe --help

# Configure the PKI client
./.venv/Scripts/pki.exe config
```

> **Note:** Live PKI credentials should be placed in `~/.config/pki-cli/.env` and should never be committed.

## Troubleshooting

The project path may contain spaces and Vietnamese characters. If Windows console output fails on Unicode during script execution, enforce UTF-8 encoding:

```bat
chcp 65001
set PYTHONIOENCODING=utf-8
.venv\Scripts\python.exe scripts\wordcount.py
```
