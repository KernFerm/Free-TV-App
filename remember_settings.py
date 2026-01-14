"""
remember_settings.py - Persistent last channel and volume for Enhanced TV App
"""

import os
import json

class RememberSettings:
    def __init__(self, settings_file='user_settings.json'):
        self.settings_file = settings_file
        self.data = {'last_channel': None, 'volume': 100}
        self.load()
        self.sanitize()

    def load(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception:
                pass
        self.sanitize()

    def sanitize(self):
        # Ensure last_channel is a string or None
        if not isinstance(self.data.get('last_channel'), (str, type(None))):
            self.data['last_channel'] = None
        # Ensure volume is an int between 0 and 100
        try:
            v = int(self.data.get('volume', 100))
            if not (0 <= v <= 100):
                v = 100
            self.data['volume'] = v
        except Exception:
            self.data['volume'] = 100

    def save(self):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass

    def set_last_channel(self, channel_url):
        self.data['last_channel'] = channel_url
        self.save()

    def set_volume(self, volume):
        self.data['volume'] = volume
        self.save()

    def get_last_channel(self):
        return self.data.get('last_channel')

    def get_volume(self):
        return self.data.get('volume', 100)
