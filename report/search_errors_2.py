import pathlib

file_path = pathlib.Path(__file__).parent / "slide.tex"
lines = file_path.read_text(encoding="utf-8").splitlines()

for i, line in enumerate(lines, 1):
    if ">" in line and not "latex" in line.lower() and not "pdflatex" in line.lower():
        print(f"Line {i}: {line}")
