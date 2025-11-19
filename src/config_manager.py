import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "work_duration": 50,  # minutes
    "rest_duration": 5,   # minutes
    "sound_enabled": True,
    "stats": {
        "total_rests": 0,
        "today_rests": 0,
        "last_reset_date": ""
    }
}

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()
        self.check_daily_reset()

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return DEFAULT_CONFIG.copy()
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                # Merge with default to ensure new keys exist
                for key, value in DEFAULT_CONFIG.items():
                    if key not in data:
                        data[key] = value
                return data
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

    def check_daily_reset(self):
        import datetime
        today = datetime.date.today().isoformat()
        stats = self.config.get("stats", DEFAULT_CONFIG["stats"])
        
        if stats.get("last_reset_date") != today:
            stats["today_rests"] = 0
            stats["last_reset_date"] = today
            self.set("stats", stats)

    def increment_rest_count(self):
        self.check_daily_reset()
        stats = self.config.get("stats", DEFAULT_CONFIG["stats"])
        stats["total_rests"] += 1
        stats["today_rests"] += 1
        self.set("stats", stats)
