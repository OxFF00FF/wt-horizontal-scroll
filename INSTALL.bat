@echo off
chcp 65001 >nul

if not defined WT_SESSION (
    wt.exe -p "Command Prompt" cmd /k "%~f0"
    exit /b
)

set "SCRIPT_DIR=%~dp0"
echo 📂  Current dir: %cd%
echo 📂  Script dir:  %SCRIPT_DIR%
echo.

if not exist "%SCRIPT_DIR%.venv" (
    echo 🔄  Creating virtual environment...
    python -m venv "%SCRIPT_DIR%.venv"
    echo ✔️  Virtual environment created
    echo.
)

echo 🔄  Activating virtual environment...
call "%SCRIPT_DIR%.venv\Scripts\activate"
echo ✔️ Virtual environment activated
echo.

echo 🔄  Updating pip...
python -m pip install --upgrade pip
echo ✔️  Pip is updated to latest version
echo.

echo 🔄  Installing dependencies...
pip install -r "%SCRIPT_DIR%requirements.txt"
playwright install chromium

echo ✔️  Required dependencies installed
echo.

pause

exit