@echo off
cd /d "%~dp0"
echo ===== %date% %time% >> log.txt
".venv\Scripts\python.exe" src\perbarui.py >> log.txt 2>&1
".venv\Scripts\python.exe" src\laporan.py >> log.txt 2>&1