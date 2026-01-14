"""
theme_toggle.py - Modular dark/light theme toggle for Enhanced TV App
"""

from PyQt5.QtGui import QPalette, QColor

def sanitize_theme(theme):
    return theme if theme in ('dark', 'light') else 'dark'

def set_theme(app, theme='dark'):
    theme = sanitize_theme(theme)
    if theme == 'dark':
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 32, 36))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        app.setPalette(palette)
    else:
        app.setPalette(QPalette())
