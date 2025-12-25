@echo off
chcp 65001 >nul
title Setup InstructPix2Pix Studio

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║         🔧 Setup InstructPix2Pix Studio                  ║
echo ║         AMD 6800XT + Ryzen 5950X                         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python не найден! Установи Python 3.10+
    pause
    exit /b 1
)

echo [1/4] Создание виртуального окружения...
if not exist "venv_win" (
    python -m venv venv_win
    echo      ✓ venv создан
) else (
    echo      ✓ venv уже существует
)

echo.
echo [2/4] Активация venv...
call venv_win\Scripts\activate.bat

echo.
echo [3/4] Обновление pip...
python -m pip install --upgrade pip --quiet

echo.
echo [4/4] Установка зависимостей (это займёт несколько минут)...
pip install -r requirements-windows.txt

if errorlevel 1 (
    echo.
    echo [!] Ошибка установки зависимостей!
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║         ✅ Установка завершена!                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo Для запуска используй: run.bat
echo.
pause
