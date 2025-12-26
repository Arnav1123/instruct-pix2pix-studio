"""
Prompt and generation settings presets
"""

# Prompt presets
PRESETS = {
    "Watercolor": "Turn it into a watercolor painting",
    "Winter": "Make it look like winter with snow",
    "Sunset": "Add a beautiful sunset lighting",
    "Anime": "Turn into anime style artwork",
    "Oil Paint": "Transform into oil painting style",
    "Night": "Make it nighttime with moonlight",
    "Fire": "Add dramatic fire effects",
    "Underwater": "Make it look underwater",
    "Sunglasses": "Add stylish sunglasses",
    "Halloween": "Make it spooky Halloween style",
    "Christmas": "Add Christmas decorations and snow",
    "Spring": "Make it spring with cherry blossoms",
}

# Generation settings presets
SETTINGS_PRESETS = {
    "Fast": {
        "steps": 15,
        "guidance": 7.0,
        "image_cfg": 1.5,
        "description": "Quick generation, basic quality"
    },
    "Balanced": {
        "steps": 20,
        "guidance": 7.5,
        "image_cfg": 1.5,
        "description": "Optimal balance of speed and quality"
    },
    "Quality": {
        "steps": 30,
        "guidance": 8.0,
        "image_cfg": 1.3,
        "description": "Maximum quality, slower"
    },
    "Precise": {
        "steps": 25,
        "guidance": 10.0,
        "image_cfg": 1.2,
        "description": "Strict prompt adherence"
    },
    "Preserve Style": {
        "steps": 20,
        "guidance": 6.0,
        "image_cfg": 2.0,
        "description": "Maximum original preservation"
    },
}


def get_preset_names():
    """Get list of prompt preset names"""
    return list(PRESETS.keys())


def get_settings_preset_names():
    """Get list of settings preset names"""
    return list(SETTINGS_PRESETS.keys())


def get_settings_preset(name):
    """Get settings preset by name"""
    return SETTINGS_PRESETS.get(name, SETTINGS_PRESETS["Balanced"])
