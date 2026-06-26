# Public Key Infrastructure (PKI) - ATTT Course Project

[![GitHub](https://img.shields.io/badge/GitHub-moonshineTP%2FATTT--20252-blue?logo=github)](https://github.com/moonshineTP/ATTT-20252)
[![LaTeX](https://img.shields.io/badge/LaTeX-47A141?logo=latex&logoColor=white)](https://www.latex-project.org/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Overview

This repository contains the course project for "Nhập môn An toàn thông tin" (Introduction to Information Security)
at Hanoi University of Science and Technology (HUST). The project focuses on Public Key Infrastructure (PKI) and
features a LaTeX academic report, a Beamer slide presentation, and a miniature PKI demonstration.

The academic report details the foundations of public-key cryptography, PKI architecture, the X.509 standard,
real-world deployment cases, open-source PKI systems, and future trends. A practical client-authorization session
demonstrates key lifecycle management using a Python-based command-line interface.


## Getting Started

Follow these steps to set up the environment and build the report.

### Installation

This repository contains a pre-configured Python virtual environment (`.venv`) for Windows. To run the analysis
scripts or utilize the PKI CLI client, you should ensure Python is installed and execute commands through
the virtual environment.

To install dependencies manually if needed:

```powershell
.\.venv\Scripts\pip.exe install -r requirements.txt
```

### Usage

#### Document Verification

You can check the health of the LaTeX document, including references and citations, by running the validation script:

```powershell
$env:PYTHONIOENCODING="utf-8"
.\.venv\Scripts\python.exe scripts\check_latex.py
```

To calculate the current word count of the report:

```powershell
$env:PYTHONIOENCODING="utf-8"
.\.venv\Scripts\python.exe scripts\wordcount.py
```

#### Compiling the Report

Compile the LaTeX source files to generate the PDF report using the configured build sequence:

```powershell
cd report
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
biber main
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
```

#### PKI Manager CLI

The PKI Manager command-line interface allows you to manage a Certificate Authority and perform certificate
operations.

To inspect the capabilities of the PKI client:

```powershell
 # Run PKI help command
 .\.venv\Scripts\pki.exe --help
```

To configure the CLI:

```powershell
 # Run PKI configuration command
 .\.venv\Scripts\pki.exe config
```

> [!NOTE]
> Sensitive configuration values and private keys must be stored locally. Do not commit credentials to the
> repository.

## Repository Structure

```text
attt/
├── material/               # Source PDFs and literature references
├── report/                 # Academic LaTeX report source files
│   ├── assets/             # Images and visual diagrams
│   ├── chapter/            # Individual chapter LaTeX files (chap1 to chap8)
│   ├── main.pdf            # Compiled report document
│   ├── main.tex            # Principal LaTeX orchestration file
│   ├── references.bib      # BibLaTeX bibliography entries
│   ├── slide.pdf           # Compiled slide presentation
│   └── slide.tex           # Beamer slide presentation source
├── scripts/                # Python utility and validation scripts
│   ├── check_latex.py      # Script to validate citations and labels
│   └── wordcount.py        # Script to track report word counts
├── specs/                  # Chapter outlines and Vietnamese terminology specs
├── requirements.txt        # Python dependency declarations
└── README.md               # Repository documentation and instructions
```

## Reporting Issues

If you encounter formatting errors, build failures, or structural defects, please submit a report.

Please open a new issue on the [GitHub Issues](https://github.com/moonshineTP/ATTT-20252/issues) page.
Provide the details below:

- A clear explanation of the defect or proposal
- Steps to reproduce the compile or build failure
- Expected behavior versus observed output
- System environment specifications

## License

This work is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

Refer to the license page for additional attribution guidelines.

## Acknowledgements

This project was built as part of the IT4015 course at Hanoi University of Science and Technology.

We express our gratitude to the following resources:

- **PGS. TS. Nguyễn Linh Giang** for academic guidance and lectures.
- **Hanoi University of Science and Technology (HUST)** for the learning resources.
- The open-source security community for tools like OpenSSL and the PKI Manager CLI.
