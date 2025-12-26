"""
File saving, logging and management module
"""
import os
import json
from datetime import datetime
from pathlib import Path
from PIL import Image

# Save directories
OUTPUT_DIR = Path("outputs")
FAVORITES_DIR = OUTPUT_DIR / "favorites"
LOG_FILE = OUTPUT_DIR / "generation_log.json"


def ensure_dirs():
    """Create necessary directories"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    FAVORITES_DIR.mkdir(exist_ok=True)


def generate_filename(prefix="gen", ext="png"):
    """Generate unique filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{ext}"


def save_image(image: Image.Image, filename=None, quality=95, format="PNG"):
    """Save image to outputs"""
    ensure_dirs()
    
    if filename is None:
        ext = "png" if format.upper() == "PNG" else "jpg"
        filename = generate_filename("gen", ext)
    
    filepath = OUTPUT_DIR / filename
    
    if format.upper() == "JPEG":
        # Convert to RGB for JPEG
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        image.save(filepath, format="JPEG", quality=quality)
    else:
        image.save(filepath, format="PNG")
    
    return str(filepath)


def save_to_favorites(image: Image.Image, filename=None):
    """Save to favorites"""
    ensure_dirs()
    
    if filename is None:
        filename = generate_filename("fav", "png")
    
    filepath = FAVORITES_DIR / filename
    image.save(filepath, format="PNG")
    return str(filepath)


def log_generation(params: dict):
    """Log generation to JSON"""
    ensure_dirs()
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        **params
    }
    
    # Read existing log
    logs = []
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, IOError):
            logs = []
    
    logs.append(log_entry)
    
    # Limit log size (last 1000 entries)
    if len(logs) > 1000:
        logs = logs[-1000:]
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def get_generation_history():
    """Get generation history"""
    if not LOG_FILE.exists():
        return []
    
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def list_outputs():
    """List saved images"""
    ensure_dirs()
    files = list(OUTPUT_DIR.glob("*.png")) + list(OUTPUT_DIR.glob("*.jpg"))
    return sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)


def list_favorites():
    """List favorite images"""
    ensure_dirs()
    files = list(FAVORITES_DIR.glob("*.png")) + list(FAVORITES_DIR.glob("*.jpg"))
    return sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)
