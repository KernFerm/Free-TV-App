"""
keyboard_shortcuts.py - Modular keyboard shortcut setup for Enhanced TV App
"""

def sanitize_shortcut(shortcut):
    # Only allow non-empty strings, fallback to None
    return shortcut if isinstance(shortcut, str) and shortcut.strip() else None

def setup_shortcuts(window):
    from PyQt5.QtWidgets import QShortcut
    from PyQt5.QtGui import QKeySequence
    shortcuts = [
        ('Space', window.toggle_play_pause),
        ('Up', window.volume_up),
        ('Down', window.volume_down),
        ('Left', window.prev_channel),
        ('Right', window.next_channel),
    ]
    for key, handler in shortcuts:
        s = sanitize_shortcut(key)
        if s:
            QShortcut(QKeySequence(s), window, handler)
