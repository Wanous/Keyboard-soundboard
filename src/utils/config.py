import json
from pathlib import Path
import sys


class ConfigManager:

    DEFAULT_CONFIG = {

        "parameters": {

            "local_playback_enabled": True,
            "microphone_volume": 1.0
        },

        "sound_datas": {}
    }

    def __init__(self):

        self.APP_DIR    = self.get_app_dir()
        self.SOUNDS_DIR = self.APP_DIR / "sounds"
        self.CONFIG_PATH = self.APP_DIR / "config/config.json"

        self.CONFIG_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def get_app_dir(self) -> Path:
        """Retourne le dossier applicatif selon l'OS."""
        if sys.platform == "win32":
            base = Path.home() / "AppData" / "Roaming"
        elif sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path.home() / ".local" / "share"

        app_dir = base / "Soundboard"
        app_dir.mkdir(parents=True, exist_ok=True)
        return app_dir

    def load_config(self):

        if not self.CONFIG_PATH.exists():

            self.save_config(
                self.DEFAULT_CONFIG
            )

            return (
                self.DEFAULT_CONFIG.copy()
            )

        with open(
            self.CONFIG_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def save_config(self, config):

        with open(
            self.CONFIG_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                config,
                file,
                indent=4
            )