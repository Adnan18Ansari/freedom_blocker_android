import json
import os

class ConfigManager:
    """
    Manages loading and saving of configuration (blocked apps, settings).
    """
    def __init__(self, filename='config.json'):
        self.filename = filename
        self.config = {
            "blocked_apps": [],
            "schedule": {
                "start_time": "09:00",
                "end_time": "17:00",
                "enabled": False,
                "days": [0, 1, 2, 3, 4] # 0=Monday
            },
            "hardcore_mode": False
        }
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.config.update(data)
            except Exception as e:
                print(f"Error loading config: {e}")

    def save(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_blocked_apps(self):
        return self.config.get("blocked_apps", [])

    def add_blocked_app(self, package_name):
        if package_name not in self.config["blocked_apps"]:
            self.config["blocked_apps"].append(package_name)
            self.save()

    def remove_blocked_app(self, package_name):
        if package_name in self.config["blocked_apps"]:
            self.config["blocked_apps"].remove(package_name)
            self.save()

    def set_schedule(self, start, end, enabled=True):
        self.config["schedule"]["start_time"] = start
        self.config["schedule"]["end_time"] = end
        self.config["schedule"]["enabled"] = enabled
        self.save()
