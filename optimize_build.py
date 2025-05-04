import os
import sys
import shutil
import subprocess
import platform

print("=== Bắt đầu quá trình đóng gói ứng dụng ===")

# Kiểm tra môi trường
print("Kiểm tra môi trường...")
try:
    import PyInstaller
    print("✓ PyInstaller đã được cài đặt")
except ImportError:
    print("✗ PyInstaller chưa được cài đặt, đang cài đặt...")
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("✓ PyInstaller đã được cài đặt")

try:
    import requests
    print("✓ Requests đã được cài đặt")
except ImportError:
    print("✗ Requests chưa được cài đặt, đang cài đặt...")
    subprocess.call([sys.executable, "-m", "pip", "install", "requests"])

try:
    import pyautogui
    print("✓ PyAutoGUI đã được cài đặt")
except ImportError:
    print("✗ PyAutoGUI chưa được cài đặt, đang cài đặt...")
    subprocess.call([sys.executable, "-m", "pip", "install", "pyautogui"])

# Tạo thư mục build nếu chưa có
if not os.path.exists("build"):
    os.makedirs("build")

# Tạo file danh sách module cần thiết
with open("build/necessary_modules.py", "w") as f:
    f.write("""
# Danh sách các module cần thiết
import requests
import pyautogui
import configparser
import datetime
import time
import socket
import uuid
import json
import os
""")

print("\nĐang tạo file thực thi tối ưu...")

# Lấy đường dẫn Python hiện tại
python_executable = sys.executable

# Xác định cờ tùy thuộc vào hệ điều hành
console_flag = "--noconsole" if platform.system() == "Windows" else "--windowed"

# Xác định định dạng đường dẫn dựa trên hệ điều hành
path_delimiter = ";" if platform.system() == "Windows" else ":"
add_data_format = f"screenshot_client.ini{path_delimiter}."

# Chuẩn bị lệnh PyInstaller
pyinstaller_cmd = [
    python_executable, "-m", "PyInstaller",
    "--onefile",
    console_flag,
    "--clean",
    "--name=ScreenshotClient",
    "--log-level=INFO",
    f"--add-data={add_data_format}",
    "--exclude-module=numpy",
    "--exclude-module=matplotlib",
    "--exclude-module=pandas",
    "--exclude-module=scipy",
    "--exclude-module=PyQt5",
    "--exclude-module=tkinter",
    "--exclude-module=cv2",
    "--exclude-module=cryptography",
    "screenshot_client.py"
]

# Nếu UPX có sẵn, thêm tùy chọn để nén
if os.path.exists("upx") or shutil.which("upx"):
    pyinstaller_cmd.insert(5, "--upx-dir=upx" if os.path.exists("upx") else "--upx-dir=" + shutil.which("upx"))

# Thực thi lệnh PyInstaller
print("Đang chạy lệnh:", " ".join(pyinstaller_cmd))
result = subprocess.call(pyinstaller_cmd)

if result == 0:
    print("\n✓ Đã tạo thành công file thực thi!")
    
    # Kiểm tra kích thước file
    exe_name = "ScreenshotClient.exe" if platform.system() == "Windows" else "ScreenshotClient"
    exe_path = os.path.join("dist", exe_name)
    if os.path.exists(exe_path):
        size_bytes = os.path.getsize(exe_path)
        size_mb = size_bytes / (1024 * 1024)
        print(f"Kích thước file: {size_mb:.2f} MB")
    
    # Tạo thư mục cài đặt
    print("\nĐang chuẩn bị thư mục để tạo bộ cài đặt...")
    installer_dir = "installer"
    if not os.path.exists(installer_dir):
        os.makedirs(installer_dir)
    
    if platform.system() == "Windows":
        # Tạo file InnoSetup script cho Windows
        inno_script = '''
[Setup]
AppName=Screenshot Client
AppVersion=1.0
DefaultDirName={commonpf}\\Screenshot Client
DefaultGroupName=Screenshot Client
OutputBaseFilename=ScreenshotClient_Setup
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "dist\\ScreenshotClient.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "screenshot_client.ini"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist

[Icons]
Name: "{group}\\Screenshot Client"; Filename: "{app}\\ScreenshotClient.exe"
Name: "{commondesktop}\\Screenshot Client"; Filename: "{app}\\ScreenshotClient.exe"
Name: "{group}\\Thay đổi cấu hình"; Filename: "{app}\\screenshot_client.ini"; IconFilename: "{sys}\\shell32.dll"; IconIndex=71

[Registry]
Root: HKCU; Subkey: "Software\\Microsoft\\Windows\\CurrentVersion\\Run"; ValueType: string; ValueName: "ScreenshotClient"; ValueData: """{app}\\ScreenshotClient.exe"""; Flags: uninsdeletevalue

[Run]
Filename: "{app}\\ScreenshotClient.exe"; Description: "Chạy ứng dụng sau khi cài đặt"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "taskkill"; Parameters: "/f /im ScreenshotClient.exe"; Flags: runhidden
'''
        
        with open(os.path.join(installer_dir, "setup_script.iss"), "w") as f:
            f.write(inno_script)
            
        print("\n✓ Đã tạo file cấu hình Inno Setup!")
        print("\nĐể tạo bộ cài đặt:")
        print("1. Cài đặt Inno Setup: https://jrsoftware.org/isdl.php")
        print(f"2. Mở file {installer_dir}/setup_script.iss bằng Inno Setup")
        print("3. Build > Compile để tạo bộ cài đặt")
        print("\nBộ cài đặt sẽ được tạo trong thư mục Output/ScreenshotClient_Setup.exe")
    
    else:  # macOS/Linux
        # Tạo file cấu hình cho macOS
        if platform.system() == "Darwin":  # macOS
            # Tạo thư mục cho app
            app_dir = "installer/ScreenshotClient.app/Contents/MacOS"
            os.makedirs(app_dir, exist_ok=True)
            
            # Copy file thực thi
            shutil.copy(exe_path, os.path.join(app_dir, "ScreenshotClient"))
            
            # Copy file cấu hình
            shutil.copy("screenshot_client.ini", os.path.join(app_dir, "screenshot_client.ini"))
            
            # Tạo file plist
            plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ScreenshotClient</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.screenshotclient</string>
    <key>CFBundleName</key>
    <string>Screenshot Client</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSUIElement</key>
    <true/>
</dict>
</plist>'''
            
            # Lưu file plist
            plist_dir = "installer/ScreenshotClient.app/Contents"
            with open(os.path.join(plist_dir, "Info.plist"), "w") as f:
                f.write(plist_content)
            
            # Tạo script cài đặt
            startup_script = '''#!/bin/bash
# Script cài đặt Screenshot Client

# Tạo thư mục ứng dụng
mkdir -p ~/Applications/ScreenshotClient

# Copy file
cp -R ScreenshotClient.app ~/Applications/
cp screenshot_client.ini ~/Applications/ScreenshotClient/

# Tạo file khởi động tự động
mkdir -p ~/Library/LaunchAgents
cat > ~/Library/LaunchAgents/com.example.screenshotclient.plist << 'EOL'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.screenshotclient</string>
    <key>ProgramArguments</key>
    <array>
        <string>~/Applications/ScreenshotClient.app/Contents/MacOS/ScreenshotClient</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOL

# Tải ứng dụng
launchctl load ~/Library/LaunchAgents/com.example.screenshotclient.plist

echo "Đã cài đặt Screenshot Client thành công!"
'''
            
            with open(os.path.join(installer_dir, "install.sh"), "w") as f:
                f.write(startup_script)
            
            # Cấp quyền thực thi
            os.chmod(os.path.join(installer_dir, "install.sh"), 0o755)
            
            print("\n✓ Đã tạo .app bundle cho macOS!")
            print("\nĐể đóng gói thành bộ cài đặt cho macOS:")
            print("1. Cài đặt Packages: http://s.sudre.free.fr/Software/Packages/about.html")
            print("2. Tạo package project mới với Packages")
            print("3. Thêm .app từ thư mục installer/")
            print("\nHoặc để cài đặt trực tiếp:")
            print(f"1. Chạy: installer/install.sh")
        
        else:  # Linux
            # Tạo script cài đặt cho Linux
            install_script = '''#!/bin/bash
# Script cài đặt Screenshot Client cho Linux

# Tạo thư mục ứng dụng
mkdir -p ~/.local/bin/screenshotclient
mkdir -p ~/.local/share/applications
mkdir -p ~/.config/autostart

# Copy file
cp ScreenshotClient ~/.local/bin/screenshotclient/
cp screenshot_client.ini ~/.local/bin/screenshotclient/

# Tạo desktop file
cat > ~/.local/share/applications/screenshotclient.desktop << 'EOL'
[Desktop Entry]
Name=Screenshot Client
Comment=Client chụp màn hình tự động
Exec=~/.local/bin/screenshotclient/ScreenshotClient
Terminal=false
Type=Application
Categories=Utility;
EOL

# Tạo autostart
cp ~/.local/share/applications/screenshotclient.desktop ~/.config/autostart/

# Cấp quyền thực thi
chmod +x ~/.local/bin/screenshotclient/ScreenshotClient

echo "Đã cài đặt Screenshot Client thành công!"
'''
            
            with open(os.path.join(installer_dir, "install.sh"), "w") as f:
                f.write(install_script)
            
            # Cấp quyền thực thi
            os.chmod(os.path.join(installer_dir, "install.sh"), 0o755)
            
            print("\n✓ Đã tạo script cài đặt cho Linux!")
            print("\nĐể cài đặt trên Linux:")
            print(f"1. Chạy: installer/install.sh")
    
    # Tạo file hướng dẫn chung
    readme = '''
=== HƯỚNG DẪN SỬ DỤNG SCREENSHOT CLIENT ===

1. CÀI ĐẶT
   - Trên Windows: Chạy file ScreenshotClient_Setup.exe
   - Trên macOS: Chạy file install.sh hoặc mở file .pkg
   - Trên Linux: Chạy file install.sh
   
2. CẤU HÌNH
   - Mở file cấu hình screenshot_client.ini:
     + server_url: Địa chỉ máy chủ của bạn
     + interval: Thời gian giữa các lần chụp (giây)
     + client_name: Tên máy tính (để nhận dạng)
   
3. SỬ DỤNG
   - Ứng dụng sẽ tự động chạy sau khi cài đặt
   - Ứng dụng cũng sẽ tự động khởi động cùng hệ thống
   - Không cần thao tác gì thêm, ứng dụng chạy ngầm
   
4. KIỂM TRA
   - Xem ảnh chụp màn hình trên server
   - Địa chỉ server thường là: http://[địa_chỉ_server]/screenshot_server/
   
5. GỠ CÀI ĐẶT
   - Trên Windows: Control Panel > Programs > Uninstall a program
   - Trên macOS/Linux: Xóa các thư mục và file đã cài đặt
'''
    
    with open(os.path.join(installer_dir, "README.txt"), "w") as f:
        f.write(readme)
    
    print("\n✓ Đã tạo thành công các file cấu hình cho bộ cài đặt!")
    print(f"\nCác file đã được lưu vào thư mục: {installer_dir}")
    
else:
    print("\n✗ Không thể tạo file thực thi. Vui lòng kiểm tra lỗi ở trên.") 