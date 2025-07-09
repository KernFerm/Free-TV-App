# Free TV Player - Modern Edition

A modern, feature-rich IPTV player application with a user-friendly interface, designed to stream free TV channels from around the world. This is a standalone Windows executable that requires no Python installation.

## ⚡ Quick Start

### Prerequisites
**VLC Media Player must be installed** for video playback.

#### Installation:
1. **Download VLC**: Visit https://www.videolan.org/vlc/
2. **Install VLC**: Run the installer with default settings
3. **Alternative methods**:
   - Windows: `winget install VideoLAN.VLC`
   - Windows: Install from Microsoft Store
   - Windows: `choco install vlc` (if you have Chocolatey)

### Running the Application
1. **Install VLC Media Player** (required):
   - Run `install_vlc.bat` for automatic installation
   - Or manually download from https://www.videolan.org/vlc/

2. **Launch the Application**:
   - Navigate to the `TV` folder
   - Double-click `free_tv.exe`
   - No Python installation required!

## Features

### 🎨 Modern UI Design
- **Dark Theme**: Sleek, modern dark interface that's easy on the eyes
- **Responsive Layout**: Resizable panels with intuitive splitter
- **Professional Styling**: Modern buttons, inputs, and controls
- **Menu Bar**: Comprehensive menu system with shortcuts and actions

### 🌍 Enhanced Channel Organization
- **Country-Based Categorization**: Channels automatically grouped by country with full country names
- **Intelligent Country Detection**: Advanced algorithm that detects countries from multiple sources:
  - Channel metadata (tvg-country attribute)
  - Group titles and categories
  - Channel names and prefixes
  - Known broadcaster mappings
- **Expandable Tree View**: Navigate through countries and channels easily
- **Full Country Names**: Display proper country names (e.g., "United States (US)" instead of just "US")

### � Enhanced Video Playback
- **Real-time Search**: Search channels by name instantly
- **Country Filter**: Filter channels by specific countries with full names
- **Combined Filtering**: Search within specific countries
- **Smart Filtering**: Automatically expand matching results

### 📺 Multiple Free TV Sources
- **IPTV-Org**: Global collection of 8000+ free public channels
- **Free TV Project**: Curated collection of free-to-air channels
- **Pluto TV-style**: Free internet TV channels with various genres
- **Local Antenna/OTA**: Simulated local broadcast channels
- **News Channels**: Dedicated news sources from around the world
- **Sports Channels**: Free sports and fitness channels
- **Custom URL**: Load any M3U playlist from a URL
- **Multi-source Loading**: Combine channels from multiple sources simultaneously
- **VLC Integration**: Reliable video playback using VLC media player
- **Comprehensive Controls**: Play, pause, stop, volume, and mute
- **Channel Information**: Display current channel name and details
- **Keyboard Shortcuts**: Full keyboard control support

### 🎛️ Menu System
- **File Menu**: Open custom playlists, reload, and exit
- **View Menu**: Fullscreen mode, expand/collapse countries
- **Playback Menu**: All playback controls with shortcuts
- **Sources Menu**: Access multiple free TV sources and multi-source loading
- **Help Menu**: About dialog, keyboard shortcuts, and free TV sources info

### ⚡ Performance & Usability
- **Background Loading**: Channels load in a separate thread
- **Progress Indication**: Visual feedback during channel loading
- **Error Handling**: Graceful handling of network and playback errors
- **Keyboard Shortcuts**: Comprehensive shortcut system

## Installation

### Simple Setup (Recommended)
1. **Install VLC Media Player**:
   - Double-click `install_vlc.bat` for automatic installation
   - Or manually download from https://www.videolan.org/vlc/

2. **Run the Application**:
   - Navigate to the `TV` folder
   - Double-click `free_tv.exe`
   - Ready to use - no additional software needed!

## Usage

### Getting Started
1. Run `install_vlc.bat` to install VLC Media Player (if not already installed)
2. Navigate to the `TV` folder and double-click `free_tv.exe`
3. Wait for channels to load (progress bar will show loading status)
4. Browse channels by country in the left panel (showing full country names)
5. Search for specific channels using the search bar
6. Filter by country using the dropdown (with full country names)
7. Double-click any channel to start playing

### Accessing Different TV Sources
Use the **Sources** menu to access various free TV sources:
- **IPTV-Org**: Default source with global channels
- **Free TV Project**: Curated free-to-air channels
- **Pluto TV-style**: Internet TV channels with various genres
- **Local Antenna/OTA**: Simulated local broadcast channels (like over-the-air)
- **News Channels**: Dedicated news sources
- **Sports Channels**: Free sports and fitness content
- **Custom URL**: Load any M3U playlist from a URL
- **Multi-source Loading**: Combine channels from multiple sources for maximum variety

### Menu System
- **File Menu**: 
  - Open custom M3U playlist files
  - Reload current playlist
  - Exit application
- **View Menu**:
  - Toggle fullscreen mode
  - Expand/collapse all countries
- **Playback Menu**:
  - Play/pause controls
  - Stop playback
  - Volume controls and mute
- **Sources Menu**:
  - IPTV-Org: Global collection of free public channels
  - Free TV Project: Curated free-to-air channels
  - Pluto TV-style: Free internet TV channels
  - Local Antenna/OTA: Simulated local broadcast channels
  - News Channels: Dedicated news sources
  - Sports Channels: Free sports and fitness channels
  - Custom URL: Load any M3U playlist from a URL
  - Multi-source Loading: Combine channels from multiple sources
- **Help Menu**:
  - About dialog
  - Keyboard shortcuts reference
  - Free TV Sources Info: Details about all available sources

### Keyboard Shortcuts
- **Ctrl+O**: Open playlist file
- **F5**: Reload playlist
- **F11**: Toggle fullscreen
- **Space**: Play/Pause
- **M**: Toggle mute
- **Ctrl+↑/↓**: Volume up/down
- **Ctrl+E**: Expand all countries
- **Ctrl+Q**: Exit application
- **F1**: Show shortcuts help

### Controls
- **Play/Pause**: Toggle playback of current channel
- **Stop**: Stop playback completely
- **Volume**: Adjust audio volume with the slider
- **Mute**: Toggle audio mute
- **Search**: Type to search channels in real-time
- **Country Filter**: Select specific countries to browse

### Channel Organization
Channels are automatically organized by:
- **Country**: Detected from multiple sources including metadata, titles, and broadcaster databases
- **Full Names**: Countries shown with proper names (e.g., "United States (US)")
- **Alphabetical**: Countries and channels sorted alphabetically
- **Unknown**: Channels without clear country information grouped separately

## Quick Start Scripts

### VLC Installation Script
```batch
install_vlc.bat
```

This script automatically installs VLC Media Player using Windows Package Manager (winget) or downloads it directly if winget is not available.

## Channel Sources

The application provides access to multiple free TV sources:

### Primary Sources
- **IPTV-Org**: 8000+ free public channels worldwide with regular updates
- **Free TV Project**: Curated collection of free-to-air channels
- **Pluto TV-style**: Free internet TV channels with various genres
- **Local Antenna/OTA**: Simulated local broadcast channels (over-the-air experience)
- **News Channels**: Dedicated news sources from around the world
- **Sports Channels**: Free sports and fitness channels

### Advanced Features
- **Custom URL**: Load any M3U playlist from a URL
- **Multi-source Loading**: Combine channels from multiple sources simultaneously for maximum variety
- **Automatic Categorization**: All sources are automatically organized by country
- **Legal Compliance**: All sources contain publicly available, legal streams

## Requirements

- **VLC Media Player** (automatically installed via `install_vlc.bat`)
- **Windows Operating System**
- **Internet Connection** (for streaming channels)

## Troubleshooting
1. **Application won't start**: Ensure VLC is installed (run `install_vlc.bat`)
2. **No video playback**: Restart the application after VLC installation
3. **Slow loading**: Check internet connection
4. **Missing channels**: Some channels may be temporarily unavailable
5. **Audio issues**: Check VLC audio settings and system volume
6. **Sources not loading**: Try different sources from the Sources menu
7. **Multi-source loading slow**: Large combined playlists may take longer to load

### Error Messages
- **"Failed to load channels"**: Network connection issue or source unavailable
- **"Playback Error"**: Stream may be unavailable or VLC issue
- **"VLC not found"**: Run `install_vlc.bat` to install VLC Media Player
- **"Source loading failed"**: Try a different source or check internet connection

## Contributing

This is a demonstration application. For production use, consider:
- Adding playlist management and favorites
- Implementing channel recording capabilities
- Adding more video controls and settings
- Improving error handling and recovery
- Adding EPG (Electronic Program Guide) support
- Implementing channel recommendations

## License

This project is for educational and demonstration purposes. Please respect the terms of service of the streaming sources and ensure compliance with local laws regarding streaming content.
