@echo off
chcp 65001 >nul
title Setup InstructPix2Pix Studio

echo.
echo ========================================================
echo          Setup InstructPix2Pix Studio
echo          GPU Required (AMD DirectML / NVIDIA CUDA)
echo ========================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10+
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
if not exist "venv_win" (
    python -m venv venv_win
    echo       Done
) else (
    echo       Already exists
)

echo.
echo [2/4] Activating venv...
call venv_win\Scripts\activate.bat

echo.
echo [3/4] Updating pip...
python -m pip install --upgrade pip --quiet

echo.
echo [4/4] Installing dependencies (this may take a few minutes)...
pip install -r requirements-windows.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo ========================================================
echo          Setup Complete!
echo ========================================================
echo.
echo To launch the application, run: run.bat
echo.
pause
