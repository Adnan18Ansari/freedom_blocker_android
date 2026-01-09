# Freedom Blocker Android - Build Instructions

## Cloud Build (Recommended - No Linux Required)
If you don't have a Linux environment, you can build the APK using GitHub Actions:

1.  **Upload this folder to a GitHub Repository.**
2.  Go to the **Actions** tab in your repository.
3.  You will see the "Build Android APK" workflow running automatically (or you can manually trigger it).
4.  Once completed (approx. 15 mins), click on the workflow run.
5.  Scroll down to the **Artifacts** section and download `freedom-blocker-apk`.
6.  Unzip the file to find your `.apk` and install it on your phone.

## Local Linux Build
This project is a Python/Kivy application designed to be compiled into an Android APK using [Buildozer](https://github.com/kivy/buildozer).

## Prerequisites
- A Linux environment (Ubuntu 20.04+ recommended) or WSL (Windows Subsystem for Linux).
- Python 3
- Git
- OpenJDK 17
- Unzip/Zip

## Setup Buildozer (Linux/WSL)
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --user --upgrade buildozer
# Add ~/.local/bin to your PATH if needed
export PATH=$PATH:~/.local/bin
```

## Build the APK
1. Navigate to the project directory:
   ```bash
   cd /mnt/d/Projects/freedom_blocker_android
   ```
   *(Note: Adjust path if you copied the files elsewhere)*

2. Run Buildozer:
   ```bash
   buildozer android debug
   ```
   *This will take a while (15-30 mins) on the first run as it downloads the Android SDK/NDK.*

3. Locate the APK:
   The generated APK will be in the `bin/` directory.
   Example: `bin/FreedomBlocker-0.1-arm64-v8a-debug.apk`

## Installation
1. Connect your Android phone via USB.
2. Enable **Developer Options** and **USB Debugging** on your phone.
3. Install via ADB:
   ```bash
   adb install bin/FreedomBlocker-0.1-arm64-v8a-debug.apk
   ```

## Usage
1. Open "Freedom Blocker".
2. Grant **Usage Stats** and **Overlay** permissions when prompted (or use the buttons in the app).
3. Add a package name to block (e.g., `com.android.chrome`).
4. Click **Start Service**.
5. Try opening Chrome; it should be blocked.
