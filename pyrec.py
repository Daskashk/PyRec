#!/usr/bin/env python3
"""
PyRec: Secure Screen Recorder Script
Supports X11 and Wayland with area selection.
"""

import subprocess
import os
import sys
import json
import shutil
import re
from pathlib import Path

# Configuration
CONFIG_FILE = "pyrec_config.json"
ALLOWED_CODECS = {"libx264", "libx265", "libvpx-vp9", "aac", "libmp3lame", "libopus"}
DEFAULT_RESOLUTION = "1920x1080"

def sanitize_string(text):
    """
    Removes potentially dangerous characters from strings 
    to prevent command injection or path traversal.
    """
    return re.sub(r'[^\w\-.]', '_', str(text))

def sanitize_filename(filename):
    """Ensures the filename is safe and has an extension."""
    safe_name = sanitize_string(filename)
    if not safe_name:
        safe_name = "output"
    if "." not in safe_name:
        safe_name += ".mp4"
    return safe_name

def get_crf(calidad):
    """Maps quality string to CRF integer."""
    quality_map = {"alta": 18, "media": 23, "baja": 28, "high": 18, "medium": 23, "low": 28}
    return quality_map.get(calidad.lower(), 23)

def get_server_type():
    """Detects the display server protocol."""
    return os.getenv("XDG_SESSION_TYPE")

class ScreenRecorder:
    def __init__(self):
        self.config = {}
        self.server_type = get_server_type()
        self.geometry = None

    def check_dependencies(self):
        """Verifies required system binaries."""
        if not self.server_type:
            print("Error: Display server not detected (X11/Wayland).")
            sys.exit(1)

        deps = []
        if self.server_type == "x11":
            deps = ["ffmpeg", "slop"]
        elif self.server_type == "wayland":
            deps = ["wf-recorder", "slurp"]

        for dep in deps:
            if not shutil.which(dep):
                print(f"Error: Required dependency '{dep}' not found in PATH.")
                if dep in ["slop", "slurp"]:
                    print(f"Info: Please install '{dep}' to enable area selection.")
                sys.exit(1)

    def select_area(self):
        """Invokes slop/slurp to let the user select a screen region."""
        print("\n>>> Select the recording area on your screen...")
        try:
            if self.server_type == "x11":
                result = subprocess.run(
                    ["slop", "-f", "%wx%h+%x+%y"],
                    capture_output=True, text=True, check=True
                )
                self.geometry = result.stdout.strip()
            
            elif self.server_type == "wayland":
                result = subprocess.run(
                    ["slurp", "-f", "%wx%h+%x,%y"],
                    capture_output=True, text=True, check=True
                )
                self.geometry = result.stdout.strip()
            
            print(f"Area selected: {self.geometry}")
            return True

        except subprocess.CalledProcessError:
            print("Area selection cancelled or failed. Recording full screen.")
            self.geometry = None
            return False
        except Exception as e:
            print(f"Unexpected error during area selection: {e}")
            self.geometry = None
            return False

    def get_monitor_resolution(self):
        """Fallback to detect monitor resolution if area not selected."""
        try:
            if self.server_type == "x11":
                output = subprocess.check_output(["xrandr", "-q", "-d", ":0"], stderr=subprocess.DEVNULL).decode()
                for line in output.splitlines():
                    if " connected" in line and "*" in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if "*" in part:
                                return parts[i-1]
            elif self.server_type == "wayland":
                if shutil.which("wlr-randr"):
                    output = subprocess.check_output(["wlr-randr"]).decode()
                    for line in output.splitlines():
                        if "current" in line:
                            return line.split()[0]
        except Exception:
            pass
        return DEFAULT_RESOLUTION

    def prompt_user(self, prompt, default, type_cast=str):
        """Helper for user input with default values."""
        val = input(f"{prompt} ({default}): ").strip()
        if not val:
            return default
        try:
            return type_cast(val)
        except ValueError:
            print(f"Invalid input. Using default: {default}.")
            return default

    def configure_interactive(self, use_defaults=False):
        """Interactive configuration setup."""
        print(f"\nPyRec Configuration Mode: {'Automatic' if use_defaults else 'Custom'}")
        
        detected_res = self.get_monitor_resolution()
        
        select_opt = "n"
        if not use_defaults:
            select_opt = input("Select recording area manually? (y/n) [n]: ").lower()
        
        if select_opt == "y":
            if not self.select_area():
                self.config["resolucion"] = detected_res
        else:
            self.config["resolucion"] = detected_res

        if use_defaults:
            self.config["framerate"] = 60
            self.config["archivo_salida"] = "output.mp4"
            self.config["codec"] = "libx264"
            self.config["calidad"] = "alta"
            self.config["tasa_bits_video"] = 5000
            self.config["audio"] = True
            self.config["codec_audio"] = "aac"
            self.config["tasa_bits_audio"] = 128
            
            audio_in = input("Include system audio? (y/n) [y]: ").lower()
            self.config["audio"] = audio_in != "n"
        else:
            self.config["framerate"] = self.prompt_user("Framerate", 60, int)
            raw_filename = input(f"Output filename (output.mp4): ") or "output.mp4"
            self.config["archivo_salida"] = sanitize_filename(raw_filename)
            
            codec = self.prompt_user("Video Codec", "libx264")
            if codec not in ALLOWED_CODECS:
                print(f"Warning: Codec '{codec}' is not in the recommended list.")
            self.config["codec"] = sanitize_string(codec)
            
            self.config["calidad"] = self.prompt_user("Quality (high/medium/low)", "high")
            self.config["tasa_bits_video"] = self.prompt_user("Video Bitrate (kbps)", 5000, int)
            
            audio_in = input("Include system audio? (y/n) [n]: ").lower()
            self.config["audio"] = audio_in == "y"
            
            if self.config["audio"]:
                self.config["codec_audio"] = self.prompt_user("Audio Codec", "aac")
                self.config["tasa_bits_audio"] = self.prompt_user("Audio Bitrate (kbps)", 128, int)

    def save_config(self, filename=CONFIG_FILE):
        try:
            with open(filename, "w") as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")

    def load_config(self, filename=CONFIG_FILE):
        try:
            with open(filename, "r") as f:
                self.config = json.load(f)
            print(f"Configuration loaded from {filename}")
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    def build_command(self):
        """Constructs the secure command list for subprocess."""
        cmd = []
        
        if self.server_type == "x11":
            cmd = ["ffmpeg"]
            cmd.extend(["-f", "x11grab"])
            cmd.extend(["-framerate", str(self.config["framerate"])])
            
            if self.geometry:
                cmd.extend(["-video_size", self.geometry.split('+')[0]])
                try:
                    w_h, x, y = self.geometry.split('+')
                    input_str = f":0.0+{x},{y}"
                except ValueError:
                    input_str = ":0.0"
                cmd.extend(["-i", input_str])
            else:
                cmd.extend(["-video_size", str(self.config["resolucion"])])
                cmd.extend(["-i", ":0.0"])

            if self.config["audio"]:
                if shutil.which("pactl"):
                    cmd.extend(["-f", "pulse", "-i", "default"])
                else:
                    print("Warning: PulseAudio/Pipewire not found. Audio disabled.")

            cmd.extend([
                "-c:v", self.config["codec"],
                "-crf", str(get_crf(self.config["calidad"])),
                "-b:v", f"{self.config['tasa_bits_video']}k",
                "-preset", "ultrafast",
                "-tune", "zerolatency"
            ])
            
            if self.config["audio"]:
                cmd.extend(["-c:a", self.config["codec_audio"], "-b:a", f"{self.config['tasa_bits_audio']}k"])

            cmd.append(self.config["archivo_salida"])

        elif self.server_type == "wayland":
            cmd = ["wf-recorder"]
            
            if self.geometry:
                cmd.extend(["--geometry", self.geometry])
            
            cmd.extend(["-f", self.config["archivo_salida"]])
            cmd.extend(["-c", self.config["codec"]])
            cmd.extend(["-p", f"crf={get_crf(self.config['calidad'])}"])
            cmd.extend(["-p", f"b={self.config['tasa_bits_video']}K"])

            if self.config["audio"]:
                cmd.append("-a")

        return cmd

    def record(self):
        cmd = self.build_command()
        
        print("\n" + "="*40)
        print("PYREC STARTING RECORDING")
        print(f"Command: {' '.join(cmd)}")
        print("Press Ctrl+C to stop.")
        print("="*40 + "\n")
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"\nRecording failed with error: {e}")
        except KeyboardInterrupt:
            print("\nRecording stopped by user. Finalizing file...")
        except Exception as e:
            print(f"\nUnexpected error: {e}")

def main():
    recorder = ScreenRecorder()
    recorder.check_dependencies()
    
    print("PyRec - Screen Recorder Setup")
    print("1. Custom Configuration")
    print("2. Automatic Configuration")
    print("3. Load Saved Configuration")
    
    try:
        opcion = input("Select option: ").strip()
    except KeyboardInterrupt:
        print("\nExiting...")
        return

    if opcion == "1":
        recorder.configure_interactive(use_defaults=False)
    elif opcion == "2":
        recorder.configure_interactive(use_defaults=True)
    elif opcion == "3":
        if not recorder.load_config():
            print("No valid config found. Switching to automatic mode.")
            recorder.configure_interactive(use_defaults=True)
    else:
        print("Invalid option. Exiting.")
        return
    
    recorder.save_config()
    
    try:
        input("\nPress Enter to start recording...")
        recorder.record()
    except KeyboardInterrupt:
        print("\nCancelled.")

if __name__ == "__main__":
    main()