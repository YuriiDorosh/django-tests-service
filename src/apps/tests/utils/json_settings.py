import json
import os

def get_default_settings():
    return {
        "url": "http://localhost:8030/",
        "button": "Матраци"
    }

def read_settings():
    try:
        with open('settings.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return get_default_settings()

def write_settings(data):
    with open('settings.json', 'w') as file:
        json.dump(data, file)

def get_button_and_url():
    return read_settings()

def set_button_and_url(url, button):
    settings = {"url": url, "button": button}
    write_settings(settings)
