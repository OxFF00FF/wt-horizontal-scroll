@echo off

wt -w 0 new-tab -p "Windows PowerShell" --title PythonApp %~dp0.venv\Scripts\python.exe %~dp0main.py

taskkill /IM cmd.exe /F

pause