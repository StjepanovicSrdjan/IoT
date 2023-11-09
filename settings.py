import json

def load_settings(filePath='settings.json'):
    with open(filePath, 'r') as f:
        return json.load(f)