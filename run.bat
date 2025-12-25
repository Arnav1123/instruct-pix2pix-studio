@echo off
chcp 65001 >nul
title InstructPix2Pix Studio

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║         🎨 InstructPix2Pix Studio                        ║
echo ║         AMD 6800XT + Ryzen 5950X Edition                 ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: CPU настройки для Ryzen 5950X (28 потоков для генерации)
set OMP_NUM_THREADS=28
set MKL_NUM_THREADS=28
set OMP_WAIT_POLICY=ACTIVE

:: Проверяем venv
if not exist "venv_win\Scripts\activate.bat" (
    echo [!] Virtual environment не найден!
    echo [!] Запусти сначала: setup.bat
    pause
    exit /b 1
)

:: Активируем venv
call venv_win\Scripts\activate.bat

echo [*] Запуск приложения...
echo [*] Открой в браузере: http://localhost:7860
echo.
echo [!] Для остановки нажми Ctrl+C
echo.

:: Запуск с обработкой ошибок
python app.py

if errorlevel 1 (
    echo.
    echo [!] Приложение завершилось с ошибкой
    echo [!] Проверь установку зависимостей: pip install -r requirements-windows.txt
    pause
)
