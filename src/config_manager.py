import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "work_duration": 50,  # minutes
    "rest_duration": 5,   # minutes (not used in logic yet, but good to store)
    "sound_enabled": True
}

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return DEFAULT_CONFIG.copy()
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_CONFIG.copy()

    def save_config(self, config):
        self.config = config
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

    def get(self, key):
        return self.config.get(key, DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save_config(self.config)
