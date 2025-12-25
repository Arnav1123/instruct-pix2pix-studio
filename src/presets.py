"""
Пресеты промптов и настроек генерации
"""

# Пресеты промптов
PRESETS = {
    "🎨 Акварель": "Turn it into a watercolor painting",
    "❄️ Зима": "Make it look like winter with snow",
    "🌅 Закат": "Add a beautiful sunset lighting",
    "🎭 Аниме": "Turn into anime style artwork",
    "🖼️ Масло": "Transform into oil painting style",
    "🌙 Ночь": "Make it nighttime with moonlight",
    "🔥 Огонь": "Add dramatic fire effects",
    "🌊 Под водой": "Make it look underwater",
    "👓 Очки": "Add stylish sunglasses",
    "🎃 Хэллоуин": "Make it spooky Halloween style",
    "🎄 Рождество": "Add Christmas decorations and snow",
    "🌸 Весна": "Make it spring with cherry blossoms",
}

# Пресеты настроек генерации
SETTINGS_PRESETS = {
    "⚡ Быстрый": {
        "steps": 15,
        "guidance": 7.0,
        "image_cfg": 1.5,
        "description": "Быстрая генерация, базовое качество"
    },
    "⚖️ Баланс": {
        "steps": 20,
        "guidance": 7.5,
        "image_cfg": 1.5,
        "description": "Оптимальный баланс скорости и качества"
    },
    "💎 Качество": {
        "steps": 30,
        "guidance": 8.0,
        "image_cfg": 1.3,
        "description": "Максимальное качество, дольше"
    },
    "🎯 Точный": {
        "steps": 25,
        "guidance": 10.0,
        "image_cfg": 1.2,
        "description": "Точное следование промпту"
    },
    "🖼️ Сохранить стиль": {
        "steps": 20,
        "guidance": 6.0,
        "image_cfg": 2.0,
        "description": "Максимальное сохранение оригинала"
    },
}


def get_preset_names():
    """Получить список названий пресетов промптов"""
    return list(PRESETS.keys())


def get_settings_preset_names():
    """Получить список названий пресетов настроек"""
    return list(SETTINGS_PRESETS.keys())


def get_settings_preset(name):
    """Получить пресет настроек по имени"""
    return SETTINGS_PRESETS.get(name, SETTINGS_PRESETS["⚖️ Баланс"])
