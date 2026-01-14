"""
main.py - Enhanced TV App
Modern, professional UI for end users.
"""


import sys
import os
# Suppress VLC error output at the OS level before importing vlc (Windows only)
try:
    if os.name == 'nt':
        import msvcrt
        nul = open('nul', 'w')
        os.dup2(nul.fileno(), 2)
        sys.stderr = nul
except Exception:
    pass
import vlc
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QListWidget, QListWidgetItem, QPushButton, QComboBox, QMessageBox, QFrame, QSlider
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

import re
import requests
from keyboard_shortcuts import setup_shortcuts
from theme_toggle import set_theme
from remember_settings import RememberSettings
from favorites import FavoritesManager

class TVChannel:
    def __init__(self, title, url, country="Unknown", country_name="Unknown", logo=""):
        self.title = title
        self.url = url
        self.country = country
        self.country_name = country_name
        self.logo = logo

class TVApi:
    def __init__(self, playlist_url=None):
        self.channels = []
        if playlist_url:
            self.load_playlist(playlist_url)

    def load_playlist(self, playlist_url):
        response = requests.get(playlist_url)
        response.raise_for_status()
        self.channels = self.parse_m3u_content(response.text)
        return self.channels

    def parse_m3u_content(self, content):
        channels = []
        lines = content.splitlines()
        extinf = None
        for line in lines:
            line = line.strip()
            if line.startswith('#EXTINF:'):
                extinf = line
            elif line and not line.startswith('#') and extinf:
                channel_info = self.parse_extinf(extinf)
                channel_info['url'] = line
                channels.append(TVChannel(
                    channel_info['title'],
                    channel_info['url'],
                    channel_info['country'],
                    channel_info['country_name'],
                    channel_info['logo']
                ))
                extinf = None
        return channels

    def parse_extinf(self, extinf_line):
        channel_info = {
            'title': 'Unknown Channel',
            'country': 'Unknown',
            'country_name': 'Unknown',
            'logo': '',
            'extinf': extinf_line
        }
        try:
            # Extract title
            if ',' in extinf_line:
                title_part = extinf_line.split(',', 1)[1].strip().strip('"\'')
                if title_part:
                    channel_info['title'] = title_part[:200]
            # Extract country code from tvg-country
            country_match = re.search(r'tvg-country="([^"]*)"', extinf_line, re.IGNORECASE)
            if not country_match:
                country_match = re.search(r'tvg-country=([A-Z]{2})', extinf_line, re.IGNORECASE)
            if country_match:
                country_codes = country_match.group(1).upper().split(';')
                for country_code in country_codes:
                    country_code = country_code.strip()
                    if len(country_code) == 2 and country_code.isalpha():
                        channel_info['country'] = country_code
                        channel_info['country_name'] = self.get_country_name(country_code)
                        break
            # Try group-title for country info
            if channel_info['country'] == 'Unknown':
                group_match = re.search(r'group-title="([^"]*)"', extinf_line, re.IGNORECASE)
                if group_match:
                    group_title = group_match.group(1)
                    detected_country = self.detect_country_from_text(group_title)
                    if detected_country:
                        channel_info['country'] = detected_country[0]
                        channel_info['country_name'] = detected_country[1]
            # Try to extract country from channel title patterns
            if channel_info['country'] == 'Unknown':
                title = channel_info['title']
                title_country_match = re.match(r'\[([A-Z]{2})\]\s*(.*)', title)
                if title_country_match:
                    country_code = title_country_match.group(1).upper()
                    if len(country_code) == 2 and country_code.isalpha():
                        channel_info['country'] = country_code
                        channel_info['country_name'] = self.get_country_name(country_code)
                        channel_info['title'] = title_country_match.group(2).strip()
                elif '(' in title and ')' in title:
                    paren_match = re.search(r'\(([A-Z]{2})\)', title)
                    if paren_match:
                        country_code = paren_match.group(1).upper()
                        if len(country_code) == 2 and country_code.isalpha():
                            channel_info['country'] = country_code
                            channel_info['country_name'] = self.get_country_name(country_code)
                            channel_info['title'] = re.sub(r'\s*\([A-Z]{2}\)', '', title).strip()
                elif ':' in title:
                    colon_match = re.match(r'([A-Z]{2}):\s*(.*)', title)
                    if colon_match:
                        country_code = colon_match.group(1).upper()
                        if len(country_code) == 2 and country_code.isalpha():
                            channel_info['country'] = country_code
                            channel_info['country_name'] = self.get_country_name(country_code)
                            channel_info['title'] = colon_match.group(2).strip()
                if channel_info['country'] == 'Unknown':
                    detected_country = self.detect_country_from_text(title)
                    if detected_country:
                        channel_info['country'] = detected_country[0]
                        channel_info['country_name'] = detected_country[1]
            # Extract logo URL
            logo_match = re.search(r'tvg-logo="([^"]*)"', extinf_line, re.IGNORECASE)
            if logo_match:
                channel_info['logo'] = logo_match.group(1)
        except Exception as e:
            print(f"Error parsing EXTINF: {e}")
        return channel_info

    def get_country_name(self, country_code):
        country_map = {
            'US': 'United States', 'GB': 'United Kingdom', 'CA': 'Canada', 'FR': 'France', 'DE': 'Germany',
            'IT': 'Italy', 'ES': 'Spain', 'RU': 'Russia', 'CN': 'China', 'JP': 'Japan', 'KR': 'South Korea',
            'IN': 'India', 'BR': 'Brazil', 'MX': 'Mexico', 'AU': 'Australia', 'NL': 'Netherlands',
            'SE': 'Sweden', 'NO': 'Norway', 'FI': 'Finland', 'DK': 'Denmark', 'PL': 'Poland',
            'TR': 'Turkey', 'GR': 'Greece', 'PT': 'Portugal', 'AR': 'Argentina', 'CL': 'Chile',
            'ZA': 'South Africa', 'EG': 'Egypt', 'NG': 'Nigeria', 'UA': 'Ukraine', 'RO': 'Romania',
            'HU': 'Hungary', 'CZ': 'Czech Republic', 'SK': 'Slovakia', 'BG': 'Bulgaria', 'RS': 'Serbia',
            'HR': 'Croatia', 'SI': 'Slovenia', 'AT': 'Austria', 'CH': 'Switzerland', 'BE': 'Belgium',
            'IE': 'Ireland', 'NZ': 'New Zealand', 'IL': 'Israel', 'SA': 'Saudi Arabia', 'AE': 'UAE',
            'IR': 'Iran', 'IQ': 'Iraq', 'PK': 'Pakistan', 'ID': 'Indonesia', 'TH': 'Thailand',
            'VN': 'Vietnam', 'MY': 'Malaysia', 'SG': 'Singapore', 'PH': 'Philippines', 'TW': 'Taiwan',
            'HK': 'Hong Kong', 'XX': 'Unknown'
        }
        return country_map.get(country_code, 'Unknown')

    def get_countries(self):
        countries = set()
        for c in self.channels:
            if c.country and c.country.strip() and c.country.strip().lower() != 'unknown':
                countries.add(c.country.strip())
        return sorted(countries)

    def detect_country_from_text(self, text):
        if not text:
            return None
        text_lower = text.lower().strip()
        country_name_map = {
            'united states': 'US', 'usa': 'US', 'america': 'US', 'american': 'US',
            'united kingdom': 'GB', 'uk': 'GB', 'britain': 'GB', 'british': 'GB', 'england': 'GB', 'english': 'GB',
            'canada': 'CA', 'canadian': 'CA', 'france': 'FR', 'french': 'FR', 'germany': 'DE', 'german': 'DE',
            'italy': 'IT', 'italian': 'IT', 'spain': 'ES', 'spanish': 'ES',
            'russia': 'RU', 'russian': 'RU', 'china': 'CN', 'chinese': 'CN', 'japan': 'JP', 'japanese': 'JP',
            'south korea': 'KR', 'korea': 'KR', 'korean': 'KR', 'india': 'IN', 'indian': 'IN',
            'brazil': 'BR', 'brazilian': 'BR', 'mexico': 'MX', 'mexican': 'MX', 'australia': 'AU', 'australian': 'AU',
            'netherlands': 'NL', 'dutch': 'NL', 'sweden': 'SE', 'swedish': 'SE', 'norway': 'NO', 'norwegian': 'NO',
            'finland': 'FI', 'finnish': 'FI', 'denmark': 'DK', 'danish': 'DK', 'poland': 'PL', 'polish': 'PL',
            'turkey': 'TR', 'turkish': 'TR', 'greece': 'GR', 'greek': 'GR', 'portugal': 'PT', 'portuguese': 'PT',
            'argentina': 'AR', 'argentine': 'AR', 'chile': 'CL', 'chilean': 'CL', 'south africa': 'ZA',
            'egypt': 'EG', 'egyptian': 'EG', 'nigeria': 'NG', 'nigerian': 'NG', 'ukraine': 'UA', 'ukrainian': 'UA',
            'romania': 'RO', 'romanian': 'RO', 'hungary': 'HU', 'hungarian': 'HU', 'czech republic': 'CZ', 'czech': 'CZ',
            'slovakia': 'SK', 'slovak': 'SK', 'bulgaria': 'BG', 'bulgarian': 'BG', 'serbia': 'RS', 'serbian': 'RS',
            'croatia': 'HR', 'croatian': 'HR', 'slovenia': 'SI', 'slovenian': 'SI', 'austria': 'AT', 'austrian': 'AT',
            'switzerland': 'CH', 'swiss': 'CH', 'belgium': 'BE', 'belgian': 'BE', 'ireland': 'IE', 'irish': 'IE',
            'new zealand': 'NZ', 'israel': 'IL', 'israeli': 'IL', 'saudi arabia': 'SA', 'uae': 'AE',
            'iran': 'IR', 'iranian': 'IR', 'iraq': 'IQ', 'iraqi': 'IQ', 'pakistan': 'PK', 'pakistani': 'PK',
            'indonesia': 'ID', 'indonesian': 'ID', 'thailand': 'TH', 'thai': 'TH', 'vietnam': 'VN', 'vietnamese': 'VN',
            'malaysia': 'MY', 'malaysian': 'MY', 'singapore': 'SG', 'philippines': 'PH', 'filipino': 'PH',
            'taiwan': 'TW', 'taiwanese': 'TW', 'hong kong': 'HK', 'belarus': 'BY', 'belarusian': 'BY',
        }
        for name, code in country_name_map.items():
            if name in text_lower:
                return (code, self.get_country_name(code))
        return None
# --- End Integrated TV API Logic ---

DEFAULT_PLAYLIST = "https://iptv-org.github.io/iptv/index.m3u"


class EnhancedTVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced TV App")
        self.setGeometry(100, 100, 1200, 800)
        self.setFixedSize(1325, 800)
        self.resize(False, False)
        self.api = TVApi()
        self.current_theme = 'dark'
        set_theme(QApplication.instance(), self.current_theme)
        self.settings = RememberSettings()
        self.settings.sanitize()
        self.favorites = FavoritesManager()

        # --- Hardware Acceleration Mode ---
        # User override: set to 'auto' to enable detection, or set to 'd3d11va', 'dxva2', 'nvdec', 'none' to force a mode
        user_hw_accel_mode = 'auto'  # 'auto', 'd3d11va', 'dxva2', 'nvdec', 'none'

        def detect_gpu_vendor():
            try:
                if os.name == 'nt':
                    import subprocess
                    result = subprocess.check_output(['wmic', 'path', 'win32_VideoController', 'get', 'name'], stderr=subprocess.DEVNULL)
                    gpus = result.decode(errors='ignore').lower()
                    if 'nvidia' in gpus:
                        return 'nvidia'
                    elif 'amd' in gpus or 'radeon' in gpus:
                        return 'amd'
                    elif 'intel' in gpus:
                        return 'intel'
            except Exception:
                pass
            return None

        if user_hw_accel_mode == 'auto':
            vendor = detect_gpu_vendor()
            if vendor == 'nvidia':
                hardware_accel_mode = 'd3d11va'  # 'nvdec' is not always stable on Windows
            elif vendor == 'amd':
                hardware_accel_mode = 'd3d11va'
            elif vendor == 'intel':
                hardware_accel_mode = 'd3d11va'
            else:
                hardware_accel_mode = 'd3d11va'  # fallback
            gpu_info_str = f"GPU detected: {vendor if vendor else 'unknown'}\nHardware Acceleration: {hardware_accel_mode}"
            print(f"[INFO] {gpu_info_str.replace(chr(10), ' | ')}")
        else:
            hardware_accel_mode = user_hw_accel_mode
            gpu_info_str = f"GPU detection bypassed (manual override)\nHardware Acceleration: {hardware_accel_mode}"
            print(f"[INFO] {gpu_info_str.replace(chr(10), ' | ')}")

        # Show popup with GPU info for 15 seconds (non-blocking)
        from PyQt5.QtCore import QTimer
        def show_gpu_popup():
            self.gpu_popup = QMessageBox(self)
            self.gpu_popup.setWindowTitle("Hardware Info")
            self.gpu_popup.setText(gpu_info_str)
            self.gpu_popup.setStandardButtons(QMessageBox.Close)
            self.gpu_popup.setStyleSheet("QLabel{min-width:300px; font-size:15px;} QMessageBox{background:#23272e; color:#fff;}")
            self.gpu_popup.show()
            QTimer.singleShot(5000, self.gpu_popup.close)
        QTimer.singleShot(100, show_gpu_popup)  # Show after window appears

        # Optimize VLC cache to reduce freezing (network/file cache in ms)
        self.vlc_instance = vlc.Instance(
            f'--avcodec-hw={hardware_accel_mode}',
            '--network-caching=2000',   # 2 seconds network cache
            '--file-caching=2000'       # 2 seconds file cache
        )
        self.player = self.vlc_instance.media_player_new()
        self.init_ui()
        self.load_playlist(DEFAULT_PLAYLIST)
        setup_shortcuts(self)
        # Add keyboard shortcut for theme toggle (Ctrl+T)
        from PyQt5.QtWidgets import QShortcut
        from PyQt5.QtGui import QKeySequence
        QShortcut(QKeySequence('Ctrl+T'), self, self.toggle_theme)
        # Add keyboard shortcut for showing help (Ctrl+H)
        QShortcut(QKeySequence('Ctrl+H'), self, self.show_shortcuts_popup)

    def init_ui(self):
        # Apply dark modern palette
        app = QApplication.instance()
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 32, 36))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(24, 26, 30))
        dark_palette.setColor(QPalette.AlternateBase, QColor(36, 38, 42))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(36, 38, 42))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(0, 120, 212))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        if app:
            app.setPalette(dark_palette)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(24)

        # Left: Channel browser
        left_panel = QVBoxLayout()
        left_panel.setSpacing(16)

        # Exit button row (upper left)
        exit_row = QHBoxLayout()
        self.exit_button = QPushButton("Exit")
        self.exit_button.setStyleSheet('''
            QPushButton {
                background-color: #d32f2f;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        ''')
        self.exit_button.clicked.connect(self.close)
        exit_row.addWidget(self.exit_button)
        exit_row.addStretch(1)
        left_panel.addLayout(exit_row)

        # Search and country filter
        top_bar = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search channels...")
        self.search_box.setStyleSheet("QLineEdit { border-radius: 8px; padding: 8px; font-size: 15px; background: #23252a; color: #fff; }")
        self.search_box.textChanged.connect(self.update_channel_list)
        top_bar.addWidget(self.search_box)
        self.country_combo = QComboBox()
        self.country_combo.setStyleSheet("QComboBox { border-radius: 8px; padding: 8px; font-size: 15px; background: #23252a; color: #fff; }")
        self.country_combo.currentIndexChanged.connect(self.update_channel_list)
        top_bar.addWidget(self.country_combo)
        # Add Favorite button to top_bar
        self.favorite_button = QPushButton("☆ Favorite")
        self.favorite_button.setStyleSheet('''
            QPushButton {
                background-color: #222;
                color: #ffd700;
                border: none;
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444;
            }
        ''')
        self.favorite_button.clicked.connect(self.toggle_favorite)
        top_bar.addWidget(self.favorite_button)
        left_panel.addLayout(top_bar)
        # Channel list
        self.channel_list = QListWidget()
        self.channel_list.setStyleSheet("QListWidget { border-radius: 8px; font-size: 15px; background: #23252a; color: #fff; selection-background-color: #0078d4; selection-color: #fff; }")
        self.channel_list.itemDoubleClicked.connect(self.play_channel)
        self.channel_list.currentItemChanged.connect(lambda _, __: self.update_favorite_button())
        left_panel.addWidget(self.channel_list, 1)

        # Status
        self.status = QLabel()
        self.status.setStyleSheet("color: #aaa; font-size: 13px; padding: 4px;")
        left_panel.addWidget(self.status)

        # Add always-visible shortcuts panel
        self.shortcuts_panel = QLabel()
        self.shortcuts_panel.setStyleSheet("color: #00bfff; font-size: 13px; padding: 8px; background: #181a1f; border-radius: 8px;")
        self.shortcuts_panel.setText(self.get_shortcuts_text())
        self.shortcuts_panel.setWordWrap(True)
        left_panel.addWidget(self.shortcuts_panel)

        layout.addLayout(left_panel, 2)

        # Right: Video player and controls
        right_panel = QVBoxLayout()
        right_panel.setSpacing(16)
        self.video_frame = QFrame()
        self.video_frame.setFrameShape(QFrame.Box)
        self.video_frame.setStyleSheet("background-color: #111216; border-radius: 12px; border: 2px solid #23252a; box-shadow: 0 4px 24px #00000044;")
        right_panel.addWidget(self.video_frame, 8)

        # Volume slider row
        volume_row = QHBoxLayout()
        volume_label = QLabel("🔊 Volume:")
        volume_label.setStyleSheet("color: #fff; font-size: 14px; padding-right: 8px;")
        volume_row.addWidget(volume_label)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.setToolTip("Volume")
        self.volume_slider.setStyleSheet('''
            QSlider::groove:horizontal { height: 8px; background: #23252a; border-radius: 4px; }
            QSlider::handle:horizontal { background: #0078d4; border: 2px solid #fff; width: 18px; height: 18px; margin: -6px 0; border-radius: 9px; }
            QSlider::sub-page:horizontal { background: #0078d4; border-radius: 4px; }
        ''')
        self.volume_slider.valueChanged.connect(self.set_volume)
        volume_row.addWidget(self.volume_slider)

        # Audio boost (amplification) slider (must be after volume_row is defined)
        boost_label = QLabel("Boost:")
        boost_label.setStyleSheet("color: #fff; font-size: 14px; padding-left: 16px; padding-right: 8px;")
        volume_row.addWidget(boost_label)
        self.boost_slider = QSlider(Qt.Horizontal)
        self.boost_slider.setRange(100, 300)  # 100% to 300%
        self.boost_slider.setValue(100)
        self.boost_slider.setToolTip("Audio Boost (VLC Amplification)")
        self.boost_slider.setStyleSheet('''
            QSlider::groove:horizontal { height: 8px; background: #23252a; border-radius: 4px; }
            QSlider::handle:horizontal { background: #ff9800; border: 2px solid #fff; width: 18px; height: 18px; margin: -6px 0; border-radius: 9px; }
            QSlider::sub-page:horizontal { background: #ff9800; border-radius: 4px; }
        ''')
        self.boost_slider.valueChanged.connect(self.set_boost)
        volume_row.addWidget(self.boost_slider)
        right_panel.addLayout(volume_row)

        # Playback controls (future: add play/pause/stop)
        self.now_playing = QLabel("Select a channel to play.")
        self.now_playing.setStyleSheet("color: #00bfff; font-size: 18px; font-weight: 600; padding: 8px 0 0 0;")
        right_panel.addWidget(self.now_playing)

        layout.addLayout(right_panel, 5)

        # Use remembered volume for initial slider value
        self.volume_slider.setValue(self.settings.get_volume())

    def load_playlist(self, url):
        self.status.setText("Loading playlist...")
        try:
            self.api.load_playlist(url)
            self.status.setText(f"Loaded {len(self.api.channels)} channels.")
            self.country_combo.clear()
            self.country_combo.addItem("All Countries")
            countries = self.api.get_countries()
            # Add 'Unknown' if any channel has no country or is marked unknown
            if any(not c or c.strip() == '' or c.lower() == 'unknown' for c in [ch.country for ch in self.api.channels]):
                self.country_combo.addItem("Unknown")
            self.country_combo.addItems(sorted([c for c in countries if c and c.strip() and c.lower() != 'unknown']))
            self.update_channel_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status.setText("Failed to load playlist.")

    def update_channel_list(self):
        query = self.search_box.text().strip().lower()
        country = self.country_combo.currentText()
        if country == "All Countries":
            channels = self.api.channels
        elif country == "Unknown":
            channels = [c for c in self.api.channels if not getattr(c, 'country', None) or c.country.strip() == '' or c.country.lower() == 'unknown']
        else:
            channels = [c for c in self.api.channels if getattr(c, 'country', None) and c.country.strip().lower() == country.strip().lower()]
        if query:
            channels = [c for c in channels if query in c.title.lower()]
        self.channel_list.clear()
        for c in channels:
            item = QListWidgetItem(f"{c.title}  [{c.country}]\n{c.url}")
            item.setData(Qt.UserRole, c)
            self.channel_list.addItem(item)
        if not channels:
            self.channel_list.addItem(QListWidgetItem("No channels found."))

    def play_channel(self, item):
        channel = item.data(Qt.UserRole)
        if channel:
            self.now_playing.setText(f"Now Playing: {channel.title} [{channel.country}]")
            self.player.stop()
            # Set up video output
            if sys.platform.startswith('linux'):
                self.player.set_xwindow(self.video_frame.winId())
            elif sys.platform == "win32":
                self.player.set_hwnd(self.video_frame.winId())
            elif sys.platform == "darwin":
                self.player.set_nsobject(int(self.video_frame.winId()))
            # Play new stream
            media = self.vlc_instance.media_new(channel.url)
            self.player.set_media(media)
            self.player.play()
            self.settings.set_last_channel(channel.url)
            self.settings.sanitize()
            self.update_favorite_button()

    def set_volume(self, value):
        if hasattr(self, 'player'):
            self.player.audio_set_volume(value)
            self.settings.set_volume(value)
            self.settings.sanitize()
            # Also apply current boost
            self.set_boost(self.boost_slider.value() if hasattr(self, 'boost_slider') else 100)

    def set_boost(self, value):
        """
        Set VLC audio amplification (100-300%).
        """
        if hasattr(self, 'player'):
            # VLC expects boost as percent (100 = normal, 200 = double, etc.)
            try:
                self.player.audio_set_volume(self.volume_slider.value())
                self.player.audio_set_amplification(value)
            except Exception:
                pass

    def toggle_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        set_theme(QApplication.instance(), self.current_theme)
        print(f"Theme toggled to {self.current_theme}")

    def show_shortcuts_popup(self):
        shortcuts = [
            ("Space", "Play/Pause"),
            ("Up", "Volume Up"),
            ("Down", "Volume Down"),
            ("Left", "Previous Channel"),
            ("Right", "Next Channel"),
            ("Ctrl+T", "Toggle Theme"),
        ]
        msg = "Keyboard Shortcuts:\n\n" + "\n".join(f"{k}: {v}" for k, v in shortcuts)
        QMessageBox.information(self, "Keyboard Shortcuts", msg)

    def get_shortcuts_text(self):
        shortcuts = [
            ("Space", "Play/Pause"),
            ("Up", "Volume Up"),
            ("Down", "Volume Down"),
            ("Left", "Previous Channel"),
            ("Right", "Next Channel"),
            ("Ctrl+T", "Toggle Theme"),
        ]
        return "<b>Keyboard Shortcuts:</b><br>" + "<br>".join(f"<b>{k}</b>: {v}" for k, v in shortcuts)

    def toggle_favorite(self):
        item = self.channel_list.currentItem()
        if not item:
            return
        channel = item.data(Qt.UserRole)
        if not channel:
            return
        url = channel.url
        if self.favorites.is_favorite(url):
            self.favorites.remove_favorite(url)
        else:
            self.favorites.add_favorite(url)
        self.update_favorite_button()

    def update_favorite_button(self):
        item = self.channel_list.currentItem()
        if not item:
            self.favorite_button.setText("☆ Favorite")
            return
        channel = item.data(Qt.UserRole)
        if not channel:
            self.favorite_button.setText("☆ Favorite")
            return
        url = channel.url
        if self.favorites.is_favorite(url):
            self.favorite_button.setText("★ Favorited")
        else:
            self.favorite_button.setText("☆ Favorite")

    # --- Keyboard shortcut stubs ---
    def toggle_play_pause(self):
        if hasattr(self, 'player'):
            if self.player.is_playing():
                self.player.pause()
            else:
                self.player.play()

    def volume_up(self):
        if hasattr(self, 'player'):
            current = self.volume_slider.value()
            new_value = min(current + 10, 100)
            self.volume_slider.setValue(new_value)
            self.player.audio_set_volume(new_value)
            self.settings.set_volume(new_value)
            self.settings.sanitize()

    def volume_down(self):
        if hasattr(self, 'player'):
            current = self.volume_slider.value()
            new_value = max(current - 10, 0)
            self.volume_slider.setValue(new_value)
            self.player.audio_set_volume(new_value)
            self.settings.set_volume(new_value)
            self.settings.sanitize()

    def prev_channel(self):
        current_row = self.channel_list.currentRow()
        if current_row > 0:
            self.channel_list.setCurrentRow(current_row - 1)
            self.play_channel(self.channel_list.currentItem())

    def next_channel(self):
        current_row = self.channel_list.currentRow()
        if current_row < self.channel_list.count() - 1:
            self.channel_list.setCurrentRow(current_row + 1)
            self.play_channel(self.channel_list.currentItem())

if __name__ == "__main__":
    import traceback
    def excepthook(type, value, tb):
        print("\n--- Uncaught Exception ---")
        print(f"Exception: {value}")
        traceback.print_exception(type, value, tb)
        print("-------------------------\n")
        sys.stdout.flush()
        sys.stderr.flush()
    sys.excepthook = excepthook
    print("Launching Enhanced TV App...")
    sys.stdout.flush()
    app = QApplication(sys.argv)
    win = EnhancedTVApp()
    win.show()
    print("App window should now be visible (if no error above).")
    sys.stdout.flush()
    sys.exit(app.exec_())
