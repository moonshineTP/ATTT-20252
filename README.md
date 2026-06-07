# ATTT PKI Report

This repository contains a Vietnamese course report on Public Key Infrastructure (PKI) for "Nhập môn An toàn thông tin" at HUST/SOICT.

## Python environment

Use the checked-in Windows virtual environment for all Python scripts. Do not use bare `python` or `python3` for this project unless explicitly changing the environment.

PowerShell:

```powershell
.\.venv\Scripts\python.exe scripts\check_latex.py
.\.venv\Scripts\python.exe scripts\wordcount.py
```

cmd.exe:

```bat
.venv\Scripts\python.exe scripts\check_latex.py
.venv\Scripts\python.exe scripts\wordcount.py
```

WSL/bash in this workspace:

```bash
./.venv/Scripts/python.exe scripts/check_latex.py
./.venv/Scripts/python.exe scripts/wordcount.py
```

The path may contain spaces and Vietnamese characters. If Windows console output fails on Unicode, run:

```bat
chcp 65001
set PYTHONIOENCODING=utf-8
.venv\Scripts\python.exe scripts\wordcount.py
```

Installed Python packages are logged in `requirements.txt`. The project virtualenv also provides a native `pki` command for the PKI Manager CLI:

```bash
./.venv/Scripts/pki.exe --help
./.venv/Scripts/pki.exe config
```

## PKI Manager skill

A project-level Claude Code skill is installed at `.claude/skills/pki-cli`. It is used for PKI Manager operations such as CA management, certificate issuance, renewal, revocation, downloads, and CRL management.

Live PKI credentials are not stored in this repository or in the skill folder. Create them at `~/.config/pki-cli/.env` using this shape:

```bash
PKI_API_URL=https://your-pki-server.example.com/api/v1
PKI_OIDC_URL=https://your-iam-server.example.com/realms/realm/protocol/openid-connect/token
PKI_CLIENT_ID=your-client-id
PKI_CLIENT_SECRET=your-client-secret
```

`PKI_API_URL` must include `/api/v1`.

## Report build

Build from `report/` using the LaTeX sequence configured for VS Code:

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
