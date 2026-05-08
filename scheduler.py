import json
import os
from datetime import datetime

SETTINGS_FILE = "/app/data/settings.json"
STATUS_FILE = "/app/data/status.json"


def _ensure_data_dir():
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)


def load_scheduler_settings():
    _ensure_data_dir()
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    return {
        "auto_refresh": True,
        "amazon_com": True,
        "amazon_jp": True,
        "crunchyroll": True,
        "ebay": True,
    }


def save_scheduler_settings(settings):
    _ensure_data_dir()
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def get_scheduler_status():
    _ensure_data_dir()
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE) as f:
            return json.load(f)
    return {"last_mal_refresh": "Never", "last_search": "Never"}


def update_status(key):
    _ensure_data_dir()
    status = get_scheduler_status()
    status[key] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)
