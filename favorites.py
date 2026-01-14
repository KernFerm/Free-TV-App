"""
favorites.py - Persistent favorites management for Enhanced TV App
Modular, robust, and sanitized like the rest of the app modules.
"""

import os
import json

class FavoritesManager:
    """Manages persistent, sanitized favorites for TV channels."""
    def __init__(self, favorites_file='favorites.json'):
        self.favorites_file = favorites_file
        self.favorites = set()
        self.load()

    def load(self):
        if os.path.exists(self.favorites_file):
            try:
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.favorites = set(data if isinstance(data, list) else [])
            except Exception:
                self.favorites = set()
        self.sanitize()

    def save(self):
        self.sanitize()
        try:
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.favorites), f, indent=2)
        except Exception:
            pass

    def sanitize(self):
        # Only keep valid, non-empty string URLs
        self.favorites = set(f for f in self.favorites if isinstance(f, str) and f.strip())

    def add_favorite(self, channel_url):
        if isinstance(channel_url, str) and channel_url.strip():
            self.favorites.add(channel_url)
            self.save()

    def remove_favorite(self, channel_url):
        self.favorites.discard(channel_url)
        self.save()

    def is_favorite(self, channel_url):
        return channel_url in self.favorites

    def get_favorites(self):
        return list(self.favorites)
