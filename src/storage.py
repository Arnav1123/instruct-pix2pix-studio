"""
Модуль для сохранения, логирования и управления файлами
"""
import os
import json
from datetime import datetime
from pathlib import Path
from PIL import Image

# Папки для сохранения
OUTPUT_DIR = Path("outputs")
FAVORITES_DIR = OUTPUT_DIR / "favorites"
LOG_FILE = OUTPUT_DIR / "generation_log.json"


def ensure_dirs():
    """Создать необходимые папки"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    FAVORITES_DIR.mkdir(exist_ok=True)


def generate_filename(prefix="gen", ext="png"):
    """Генерация уникального имени файла"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{ext}"


def save_image(image: Image.Image, filename=None, quality=95, format="PNG"):
    """Сохранить изображение в outputs"""
    ensure_dirs()
    
    if filename is None:
        ext = "png" if format.upper() == "PNG" else "jpg"
        filename = generate_filename("gen", ext)
    
    filepath = OUTPUT_DIR / filename
    
    if format.upper() == "JPEG":
        # Конвертируем в RGB для JPEG
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        image.save(filepath, format="JPEG", quality=quality)
    else:
        image.save(filepath, format="PNG")
    
    return str(filepath)


def save_to_favorites(image: Image.Image, filename=None):
    """Сохранить в избранное"""
    ensure_dirs()
    
    if filename is None:
        filename = generate_filename("fav", "png")
    
    filepath = FAVORITES_DIR / filename
    image.save(filepath, format="PNG")
    return str(filepath)


def log_generation(params: dict):
    """Логировать генерацию в JSON"""
    ensure_dirs()
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        **params
    }
    
    # Читаем существующий лог
    logs = []
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, IOError):
            logs = []
    
    logs.append(log_entry)
    
    # Ограничиваем размер лога (последние 1000 записей)
    if len(logs) > 1000:
        logs = logs[-1000:]
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def get_generation_history():
    """Получить историю генераций"""
    if not LOG_FILE.exists():
        return []
    
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def list_outputs():
    """Список сохранённых изображений"""
    ensure_dirs()
    files = list(OUTPUT_DIR.glob("*.png")) + list(OUTPUT_DIR.glob("*.jpg"))
    return sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)


def list_favorites():
    """Список избранных изображений"""
    ensure_dirs()
    files = list(FAVORITES_DIR.glob("*.png")) + list(FAVORITES_DIR.glob("*.jpg"))
    return sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)
