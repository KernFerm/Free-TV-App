


![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![VLC Required](https://img.shields.io/badge/VLC-Required-orange?logo=vlc-media-player)
![License](https://img.shields.io/badge/License-MIT-green)
![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)



# 📺 Enhanced TV App

**Enhanced TV App is a modern desktop application that lets you watch live TV streams from around the world, right on your computer.**

With a beautiful, easy-to-use interface, you can:
- Browse and search thousands of TV channels from online playlists (like iptv-org)
- Filter channels by country
- Play any channel instantly in the built-in video player (powered by VLC)
- Save your favorite channels for quick access
- Enjoy keyboard shortcuts for fast control (play/pause, volume, next/previous channel, theme toggle, and more)
- Switch between dark and light themes
- The app remembers your last played channel and your volume settings

**How it works:**
Just launch the app, and it will automatically load a public playlist of TV channels. You can search, filter, and play channels with a double-click. Favorites and settings are saved automatically.

---

**Can I use this on Linux or Mac?**

Yes! The Enhanced TV App is written in Python and uses PyQt5 and VLC, which are available on Windows, Linux, and macOS. You will need to have Python, VLC, and the required Python packages installed on your system. Some features (like hardware acceleration detection) are Windows-specific, but the core app works cross-platform.

---


Welcome to the Enhanced TV App! 🎉 This simple program lets you watch your favorite TV streams on your computer, save your favorite channels, and customize your viewing experience.


## ✨ What Can This App Do?

- 📡 **Watch TV Streams:** Play live TV streams using VLC Player.
- ⭐ **Save Favorites:** Easily save and access your favorite channels.
- ⌨️ **Keyboard Shortcuts:** Control the app quickly with your keyboard.
- 🌗 **Light or Dark Mode:** Switch between light and dark themes for comfortable viewing.
- 💾 **Remembers Your Settings:** The app remembers your preferences every time you open it.


## 🛠️ What You Need

1. 🐍 **Python**
	- This is the programming language the app uses. Download it from [python.org](https://www.python.org/downloads/).
	- When installing, make sure to check the box that says **Add Python to PATH** (this makes it easier to run Python from anywhere).

2. 🎬 **VLC Media Player**
	- The app uses VLC to play TV streams. Download it from [videolan.org](https://www.videolan.org/vlc/).

3. 📦 **Install the App's Requirements**
	- The app needs a few extra pieces (called "Python packages") to work. These are listed in a file called `requirements.txt`.


## 🚀 How to Set Up and Use the App


1. 📥 **Download the App**
	- Put the `enhanced-tv-app` folder anywhere you like on your computer.

2. 🛠️ **Install What the App Needs**
	- Open the `enhanced-tv-app` folder.
	- In the address bar at the top, type `cmd` and press Enter. This opens a command window in the right place.
	- Type this and press Enter:
	  ```
	  pip install -r requirements.txt
	  ```
	- Or, you can use a batch file (see below) to do this with a double-click.

3. ▶️ **Start the App**
	- In the same command window, type:
	  ```
	  python main.py
	  ```



## ⚡ Easy Install with a Batch File

We've included a file called `install_requirements.bat` in the app folder for you. 🖱️

Just double-click this file to automatically install everything the app needs.

---


**❓ Need Help?**

If you have trouble, make sure you have Python and VLC installed, and that you followed the steps above. Enjoy your enhanced TV experience! 🎈
