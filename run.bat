@echo off
chcp 65001 >nul
title InstructPix2Pix Studio

echo.
echo ========================================================
echo          InstructPix2Pix Studio
echo          AI-Powered Image Editing
echo ========================================================
echo.

:: Check venv
if not exist "venv_win\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo [ERROR] Please run setup.bat first
    pause
    exit /b 1
)

:: Activate venv
call venv_win\Scripts\activate.bat

echo [*] Starting application...
echo [*] Open in browser: http://localhost:7860
echo.
echo [*] Press Ctrl+C to stop
echo.

:: Launch
python app.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application crashed
    echo [ERROR] Check dependencies: pip install -r requirements-windows.txt
    pause
)
