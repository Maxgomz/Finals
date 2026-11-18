@echo off
cd /d "%~dp0"
python Finals.py
if errorlevel 1 (
    echo.
    echo Python could not start the application.
    echo Make sure Python 3 is installed and try again.
    pause
)
