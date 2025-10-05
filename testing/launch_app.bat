@echo off
REM Quick launcher script for the Integrated Testing App (Windows)

echo ================================
echo 🚀 Zeyta Integrated Testing App
echo ================================
echo.
echo Starting the testing interface...
echo.

cd /d "%~dp0"
python integrated_app.py

echo.
echo Goodbye! 👋
pause
