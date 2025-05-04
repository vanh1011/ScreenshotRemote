import os
import time
import requests
import pyautogui
import socket
import json
from datetime import datetime
import configparser
import uuid

# Đọc cấu hình từ file
config = configparser.ConfigParser()
config_file = 'screenshot_client.ini'

# Tạo cấu hình mặc định nếu file không tồn tại
if not os.path.exists(config_file):
    config['SERVER'] = {
        'server_url': 'http://192.168.1.100/screenshot_server/upload.php',
        'interval': '60'  # Chụp mỗi 60 giây
    }
    config['CLIENT'] = {
        'client_id': str(uuid.uuid4()),  # Tạo ID duy nhất cho máy
        'client_name': socket.gethostname()
    }
    with open(config_file, 'w') as f:
        config.write(f)
    print(f"Đã tạo file cấu hình mới: {config_file}")
else:
    config.read(config_file)
    print(f"Đã đọc file cấu hình: {config_file}")

# Đọc cấu hình
SERVER_URL = config['SERVER']['server_url']
INTERVAL = int(config['SERVER']['interval'])
CLIENT_ID = config['CLIENT']['client_id']
CLIENT_NAME = config['CLIENT']['client_name']

print(f"Client ID: {CLIENT_ID}")
print(f"Client Name: {CLIENT_NAME}")
print(f"Server URL: {SERVER_URL}")
print(f"Interval: {INTERVAL} seconds")

# Tạo thư mục lưu ảnh tạm nếu chưa có
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

def take_screenshot():
    """Chụp ảnh màn hình và lưu vào thư mục tạm thời"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/screenshot_{timestamp}.png"
    
    try:
        # Chụp màn hình
        screenshot = pyautogui.screenshot()
        # Lưu ảnh và đóng ngay lập tức
        screenshot.save(filename)
        # Giải phóng tài nguyên
        screenshot.close()
        print(f"Đã chụp màn hình: {filename}")
        return filename
    except Exception as e:
        print(f"Lỗi khi chụp màn hình: {str(e)}")
        return None

def upload_screenshot(filename):
    """Gửi ảnh màn hình lên server"""
    if not filename:
        return False
    
    try:
        # Chuẩn bị dữ liệu
        with open(filename, 'rb') as f:
            files = {'screenshot': f}
            data = {
                'client_id': CLIENT_ID,
                'client_name': CLIENT_NAME,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"Đang gửi ảnh lên server: {SERVER_URL}")
            
            # Gửi lên server với timeout để tránh treo
            response = requests.post(SERVER_URL, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('success'):
                        print(f"Đã gửi ảnh thành công: {filename}")
                        # Đợi một chút trước khi xóa file
                        time.sleep(1)
                        try:
                            os.remove(filename)
                            print(f"Đã xóa file tạm: {filename}")
                        except Exception as e:
                            print(f"Không thể xóa file: {str(e)}")
                        return True
                    else:
                        print(f"Lỗi từ server: {result.get('message')}")
                except ValueError as e:
                    print(f"Phản hồi không phải JSON: {response.text}")
                    print(f"Lỗi: {str(e)}")
            else:
                print(f"Lỗi HTTP: {response.status_code} - {response.text}")
            
            return False
    except requests.exceptions.ConnectionError as e:
        print(f"Lỗi kết nối đến server: {str(e)}")
        print("Kiểm tra lại địa chỉ server và đảm bảo server đang chạy")
        return False
    except requests.exceptions.Timeout as e:
        print(f"Timeout khi kết nối đến server: {str(e)}")
        return False
    except Exception as e:
        print(f"Lỗi khi gửi ảnh: {str(e)}")
        return False

def main():
    print("Bắt đầu chương trình chụp màn hình...")
    try:
        while True:
            # Chụp màn hình
            screenshot_file = take_screenshot()
            
            # Gửi lên server
            if screenshot_file:
                upload_screenshot(screenshot_file)
            
            # Chờ đến lần chụp tiếp theo
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Chương trình bị dừng bởi người dùng")

if __name__ == "__main__":
    main() 