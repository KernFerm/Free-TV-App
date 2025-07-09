@echo off
echo Installing VLC Media Player...
echo.
echo This script will install VLC Media Player which is required for Free TV Player.
echo.
pause

:: Try to install VLC using winget first
echo Trying to install VLC using Windows Package Manager (winget)...
winget install VideoLAN.VLC

if %errorlevel% neq 0 (
    echo.
    echo winget failed or not available. Trying chocolatey...
    choco install vlc -y
    
    if %errorlevel% neq 0 (
        echo.
        echo Automatic installation failed. Please install VLC manually:
        echo 1. Go to https://www.videolan.org/vlc/
        echo 2. Download VLC for Windows
        echo 3. Install with default settings
        echo 4. Restart Free TV Player
        echo.
        echo Or install from Microsoft Store: search for "VLC"
        pause
        exit /b 1
    )
)

echo.
echo VLC Media Player has been installed successfully!
echo You can now run Free TV Player.
echo.
pause
