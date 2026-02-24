# ffmpeg_screencap

This script allows you to record your computer screen easily and intuitively using ffmpeg, with robust security and area selection support.

* [Requirements](#requirements)
* [Usage](#usage)
* [Installation](#installation)
* [Troubleshooting](#troubleshooting)
* [Contact](#contact)
* [Especial](#especial)

## Requirements

To use this script, you must:
- Have **Python 3.X** installed on your system.
- Install **ffmpeg** on your system.
- **For X11 users**:
  - `xrandr` (for resolution detection).
  - `slop` (required for interactive area selection).
- **For Wayland users**:
  - `wlr-randr` (for resolution detection).
  - `wf-recorder` (the recording backend for Wayland).
  - `slurp` (required for interactive area selection).
- Copy the `ffmpeg_screencap.py` file to a directory and make it executable (`chmod +x ffmpeg_screencap.py`).

## Usage

To use the script, simply run the command `python3 ffmpeg_screencap.py` in your terminal.

The script will guide you through three configuration modes:
1. **Custom Configuration**: Allows you to manually set all parameters.
2. **Automatic Configuration**: Uses recommended defaults and only asks for essential options (like audio).
3. **Load Configuration**: Loads settings from a previously saved `config.json` file.

### Interactive Area Selection
When choosing "Custom Configuration", the script will ask if you want to **select the recording area**.
- If you select **Yes**, a selection tool will appear (handled by `slop` on X11 or `slurp` on Wayland). Use your mouse to draw the rectangle you wish to record.
- If you select **No**, the entire screen will be recorded based on the detected resolution.

### Default Parameters
The default values are as follows:
  - **Resolution**: Automatically detected via `xrandr` or `wlr-randr`.
  - **Framerate**: 60 fps
  - **Output File**: "output.mp4"
  - **Video Codec**: "libx264"
  - **Quality**: "high" (CRF 18)
  - **Video Bitrate**: 5000 kbps
  - **Audio**: Yes (System Audio)
  - **Audio Codec**: "aac"
  - **Audio Bitrate**: 128 kbps

## Installation

You can install the necessary dependencies on the following distributions using the commands below (run as root or with `sudo`):

### Dependencies, most be run as root when necesary:

*   **Ubuntu/Debian**: `apt install ffmpeg`
*   **Fedora/CentOS**: `dnf install ffmpeg`
*   **Arch/Manjaro**: `pacman -S ffmpeg`
*   **OpenSUSE**: `zypper install ffmpeg`
*   **Gentoo**: `emerge ffmpeg`
*   **Void Linux**: `xbps-install -S ffmpeg`
*   **Slackware**: `slackpkg install ffmpeg`
*   **Oracle Linux**: `yum install ffmpeg`
*   **Solus**: `eopkg install ffmpeg`
*   **Alpine Linux**: `apk add ffmpeg`
*   **FreeBSD**: `pkg install ffmpeg`
*   **OpenBSD**: `pkg_add ffmpeg`
*   **Mageia**: `urpmi ffmpeg`
*   **PCLinuxOS**: `apt-get install ffmpeg`
*   **OpenMandriva**: `dnf install ffmpeg`
*   **Homebrew**: `brew install ffmpeg`

### Additional Tools Required for Area Selection & Wayland:

*   **Ubuntu/Debian**: `apt install slop slurp wf-recorder`
*   **Arch/Manjaro**: `pacman -S slop slurp wf-recorder`
*   **Fedora**: `dnf install slop slurp wf-recorder` (Note: `wf-recorder` might require a COPR repo on some Fedora versions).
*   **OpenSUSE**: `zypper install slop slurp wf-recorder`
*   **Gentoo**: `emerge slop slurp wf-recorder`
*   **Void Linux**: `xbps-install -S slop slurp wf-recorder`
*   **Slackware**: `slackpkg install slop slurp wf-recorder`
*   **Oracle Linux**: `yum install slop slurp wf-recorder`
*   **Solus**: `eopkg install slop slurp wf-recorder`
*   **Alpine Linux**: `apk add slop slurp wf-recorder`
*   **FreeBSD**: `pkg install slop slurp wf-recorder`
*   **OpenBSD**: `pkg_add slop slurp wf-recorder`
*   **Mageia**: `urpmi slop slurp wf-recorder`
*   **PCLinuxOS**: `apt-get install slop slurp wf-recorder`
*   **OpenMandriva**: `dnf install slop slurp wf-recorder`
*   **Homebrew**: `brew install slop slurp wf-recorder`

**Note:** Ensure Python is installed. Most Linux distributions come with Python pre-installed. If not, install it using your distribution's package manager. 
 **⚠️ Warning**: Installing or change python version could direct to an unestable or brocken system.

## Troubleshooting

If you encounter issues, here are common solutions:

*   **"Required dependency 'slop' not found"**: You need to install `slop` (X11) or `slurp` (Wayland) to use the area selection feature.
*   **No audio in recording**:
    *   Ensure you have a PulseAudio or PipeWire server running.
    *   The script attempts to use the `pulse` backend. Verify your audio server is running.
*   **"Display server not detected"**: Ensure the environment variable `XDG_SESSION_TYPE` is set. You can check this by running `echo $XDG_SESSION_TYPE` in your terminal.
*   **Filename issues**: The script sanitizes filenames for security. If you enter a filename with special characters (like `/` or `;`), they will be replaced with underscores `_` to prevent command injection.
*   **Wayland recording fails**: Make sure `wf-recorder` is installed and you are running a Wayland compositor compatible with it (like Sway, Hyprland, or KDE/GNOME with specific configs).

## Disclaimer

This script was created primarily with Artificial Intelligence (AI) and reviewed/curated by me. It uses Python as the programming language and ffmpeg/wf-recorder as the screen capture backend.

The script was created and tested on and is intended for **GNU/Linux**. There is no support for Windows or macOS and I do not have plans to add it. It *should* work on BSD if all dependencies (ffmpeg, python, slop/slurp) are met, but this is not guaranteed.

This is a personal tool. I cannot guarantee it will work in all environments, but if you find a bug, feel free to open an issue, and I will try to fix it as soon as possible.

## Contact

If you have questions, suggestions, or want to contribute, you can contact me through:

*   **Codeberg**: Just open an [issue](https://codeberg.org/daskashk/ffmpeg_screencap/issues) with your report or questions.
*   **Matrix**: https://matrix.to/#/@narbb33:matrix.org

## Especial 

### Comunidad de habla hispana
*También tengo una comunidad de habla hispana con un fuerte enfoque en libertad, privacidad y justicia a la que están invitados:*
* *TOPIC Guild: https://matrix.to/#/#topic-guild:matrix.org*
* *FOSSS TOPIC: https://matrix.to/#/#fosstopic:matrix.org (Espacio especializado en software libre)*