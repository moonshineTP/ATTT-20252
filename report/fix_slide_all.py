import pathlib

file_path = pathlib.Path(__file__).parent / "slide.tex"
content = file_path.read_text(encoding="utf-8")

# Fix typos in slide tags
content = content.replace("\\end{itemize>", "\\end{itemize}")
content = content.replace("\\end{columns}", "\\end{column}")
content = content.replace("\\end{column reception}", "\\end{column}")
content = content.replace("\\end{columns>", "\\end{columns}")

file_path.write_text(content, encoding="utf-8")
print("Typos fixed successfully.")
