@echo off
REM Build bao cao PKI -> main.pdf
REM Chay tu thu muc report:  build.bat
REM Hoac tu goc du an:       report\build.bat

set MIKTEX=%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64
set PDFLATEX=%MIKTEX%\pdflatex.exe
set BIBER=%MIKTEX%\biber.exe

cd /d "%~dp0"

if not exist "%PDFLATEX%" (
    echo Khong tim thay pdflatex. Kiem tra MiKTeX da cai chua.
    exit /b 1
)

echo === pdflatex 1/3 ===
"%PDFLATEX%" -synctex=1 -interaction=nonstopmode -file-line-error main.tex
if errorlevel 1 echo [canh bao] co loi o lan 1, xem main.log

echo === biber ===
if exist "%BIBER%" (
    "%BIBER%" main
) else (
    echo [canh bao] khong co biber - muc tai lieu tham khao co the trong
)

echo === pdflatex 2/3 ===
"%PDFLATEX%" -synctex=1 -interaction=nonstopmode -file-line-error main.tex

echo === pdflatex 3/3 ===
"%PDFLATEX%" -synctex=1 -interaction=nonstopmode -file-line-error main.tex

if exist main.pdf (
    echo.
    echo OK: %CD%\main.pdf
) else (
    echo.
    echo LOI: khong tao duoc main.pdf
    echo Mo file main.log, tim dong bat dau bang "!"
    exit /b 1
)
