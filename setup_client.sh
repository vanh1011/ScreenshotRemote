#!/bin/bash

echo "==============================="
echo "Cài đặt Screenshot Client"
echo "==============================="
echo ""

# Kiểm tra quyền root
if [ "$(id -u)" != "0" ]; then
   echo "Vui lòng chạy script này với quyền root (sudo)"
   echo "Ví dụ: sudo ./setup_client.sh"
   exit 1
fi

# Kiểm tra Python đã được cài đặt chưa
if ! command -v python3 &> /dev/null; then
    echo "Python 3 chưa được cài đặt. Đang cài đặt..."
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        apt-get update
        apt-get install -y python3 python3-pip
    elif [ -f /etc/redhat-release ]; then
        # CentOS/RHEL
        yum install -y python3 python3-pip
    elif [ -f /etc/arch-release ]; then
        # Arch Linux
        pacman -S python python-pip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "Vui lòng cài đặt Python 3 từ https://www.python.org/downloads/"
        exit 1
    else
        echo "Không thể xác định hệ điều hành. Vui lòng cài đặt Python 3 thủ công."
        exit 1
    fi
fi

# Cài đặt các thư viện cần thiết
echo "Đang cài đặt các thư viện Python cần thiết..."
pip3 install --upgrade pip
pip3 install requests pyautogui pillow

# Tạo thư mục cài đặt
INSTALL_DIR="/opt/screenshot-client"
if [[ "$OSTYPE" == "darwin"* ]]; then
    INSTALL_DIR="/Applications/ScreenshotClient"
fi

mkdir -p "$INSTALL_DIR"

# Copy hoặc tạo file Python
echo "Đang tạo file Python client..."
cat > "$INSTALL_DIR/screenshot_client.py" << 'EOL'
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
config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshot_client.ini')

# Tạo cấu hình mặc định nếu file không tồn tại
if not os.path.exists(config_file):
    config['SERVER'] = {
        'server_url': 'http://192.168.0.123/screenshot_server/upload.php',
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
screenshot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

def take_screenshot():
    """Chụp ảnh màn hình và lưu vào thư mục tạm thời"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
    
    try:
        # Chụp màn hình
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
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
        files = {'screenshot': open(filename, 'rb')}
        data = {
            'client_id': CLIENT_ID,
            'client_name': CLIENT_NAME,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Gửi lên server
        response = requests.post(SERVER_URL, files=files, data=data)
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success'):
                    print(f"Đã gửi ảnh thành công: {filename}")
                    # Xóa file ảnh sau khi gửi thành công
                    os.remove(filename)
                    return True
                else:
                    print(f"Lỗi từ server: {result.get('message')}")
            except ValueError:
                print(f"Phản hồi không phải JSON: {response.text}")
        else:
            print(f"Lỗi HTTP: {response.status_code}")
        
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
EOL

# Cấu hình client
echo ""
echo "====== CẤU HÌNH CLIENT ======"
read -p "Nhập địa chỉ IP của máy chủ (ví dụ: 192.168.0.123): " SERVER_IP
read -p "Nhập thời gian chụp màn hình (giây, mặc định 60): " INTERVAL
if [ -z "$INTERVAL" ]; then
    INTERVAL=60
fi

read -p "Nhập tên máy tính (hiển thị trên server): " CLIENT_NAME
if [ -z "$CLIENT_NAME" ]; then
    CLIENT_NAME=$(hostname)
fi

# Tạo file cấu hình
echo "Đang tạo file cấu hình..."
cat > "$INSTALL_DIR/screenshot_client.ini" << EOL
[SERVER]
server_url = http://$SERVER_IP/screenshot_server/upload.php
interval = $INTERVAL

[CLIENT]
client_id = auto_generated
client_name = $CLIENT_NAME
EOL

# Tạo thư mục screenshots
mkdir -p "$INSTALL_DIR/screenshots"

# Tạo script chạy
cat > "$INSTALL_DIR/run_client.sh" << EOL
#!/bin/bash
cd "\$(dirname "\$0")"
python3 screenshot_client.py
EOL

chmod +x "$INSTALL_DIR/run_client.sh"

# Tạo service cho Linux
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Đang tạo service systemd..."
    cat > /etc/systemd/system/screenshot-client.service << EOL
[Unit]
Description=Screenshot Client Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 $INSTALL_DIR/screenshot_client.py
WorkingDirectory=$INSTALL_DIR
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOL

    # Hỏi người dùng có muốn bật service không
    read -p "Bạn có muốn bật service để chạy tự động khi khởi động không? (y/n): " ENABLE_SERVICE
    if [[ $ENABLE_SERVICE == "y" || $ENABLE_SERVICE == "Y" ]]; then
        systemctl enable screenshot-client.service
        systemctl start screenshot-client.service
        echo "Đã bật service thành công!"
    else
        echo "Service đã được tạo nhưng chưa bật. Để bật, hãy chạy: sudo systemctl enable screenshot-client.service"
    fi
else
    # Tạo Launch Agent cho macOS
    echo "Đang tạo Launch Agent cho macOS..."
    LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
    mkdir -p "$LAUNCH_AGENT_DIR"
    
    cat > "$LAUNCH_AGENT_DIR/com.screenshot.client.plist" << EOL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.screenshot.client</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$INSTALL_DIR/screenshot_client.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>$INSTALL_DIR</string>
    <key>StandardErrorPath</key>
    <string>$INSTALL_DIR/error.log</string>
    <key>StandardOutPath</key>
    <string>$INSTALL_DIR/output.log</string>
</dict>
</plist>
EOL

    # Hỏi người dùng có muốn bật Launch Agent không
    read -p "Bạn có muốn bật Launch Agent để chạy tự động khi đăng nhập không? (y/n): " ENABLE_AGENT
    if [[ $ENABLE_AGENT == "y" || $ENABLE_AGENT == "Y" ]]; then
        launchctl load "$LAUNCH_AGENT_DIR/com.screenshot.client.plist"
        echo "Đã bật Launch Agent thành công!"
    else
        echo "Launch Agent đã được tạo nhưng chưa bật. Để bật, hãy chạy: launchctl load ~/Library/LaunchAgents/com.screenshot.client.plist"
    fi
fi

# Hoàn tất
echo ""
echo "====== CÀI ĐẶT HOÀN TẤT ======"
echo "Chương trình đã được cài đặt tại: $INSTALL_DIR"
echo "Để chạy thủ công, hãy chạy: $INSTALL_DIR/run_client.sh"
echo ""

# Hỏi người dùng có muốn chạy ngay không
read -p "Bạn có muốn chạy chương trình ngay không? (y/n): " RUN_NOW
if [[ $RUN_NOW == "y" || $RUN_NOW == "Y" ]]; then
    cd "$INSTALL_DIR"
    python3 screenshot_client.py &
    echo "Đã khởi động chương trình trong nền!"
fi

echo ""
echo "Cảm ơn bạn đã cài đặt Screenshot Client!" 