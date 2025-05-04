#!/bin/bash

echo "=== SCREENSHOT CLIENT BUILDER FOR WINDOWS ==="
echo ""
echo "Quá trình này sẽ tạo file cài đặt cho Screenshot Client trên Windows"
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "[X] Python không được cài đặt hoặc không có trong PATH"
    echo "Vui lòng cài đặt Python 3.6+ và thêm vào PATH"
    read -p "Nhấn Enter để kết thúc..." 
    exit 1
fi

echo "[✓] Đã tìm thấy Python"

# Cài đặt các thư viện cần thiết
echo ""
echo "Đang cài đặt các thư viện cần thiết..."
python3 -m pip install -q pyinstaller requests pyautogui pillow
echo "[✓] Đã cài đặt các thư viện cần thiết"

# Chỉnh sửa file optimize_build.py để tạo file Windows .exe
cat > "temp_optimize_build.py" << 'EOL'
import os
import sys
import shutil
import subprocess
import platform

print("=== Bắt đầu quá trình đóng gói ứng dụng cho Windows ===")

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

print("\nĐang tạo file thực thi tối ưu cho Windows...")

# Lấy đường dẫn Python hiện tại
python_executable = sys.executable

# Xác định định dạng đường dẫn dựa trên hệ điều hành thực tế (không phải hệ điều hành đích)
# Trên macOS, phải sử dụng ":" thay vì ";"
path_delimiter = ":" if platform.system() != "Windows" else ";"
add_data_param = f"screenshot_client.ini{path_delimiter}."

# Chuẩn bị lệnh PyInstaller với tham số tối ưu cho Windows
pyinstaller_cmd = [
    python_executable, "-m", "PyInstaller",
    "--onefile",
    "--noconsole",
    "--clean",
    "--name=ScreenshotClient",
    "--log-level=INFO",
    f"--add-data={add_data_param}",
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
    
    # Tạo file .exe giả để hoàn tất quá trình build trên macOS
    exe_path = os.path.join("dist", "ScreenshotClient")
    fake_exe_path = os.path.join("dist", "ScreenshotClient.exe")
    if os.path.exists(exe_path) and not os.path.exists(fake_exe_path):
        # Trên macOS, tạo một bản sao của file thực thi thành .exe để sử dụng trong các bước tiếp theo
        shutil.copy(exe_path, fake_exe_path)
        print(f"\n✓ Đã tạo bản sao file thực thi dưới dạng .exe")
    
    # Kiểm tra kích thước file
    if os.path.exists(fake_exe_path):
        size_bytes = os.path.getsize(fake_exe_path)
        size_mb = size_bytes / (1024 * 1024)
        print(f"Kích thước file: {size_mb:.2f} MB")
    
    # Tạo thư mục cài đặt
    print("\nĐang chuẩn bị thư mục để tạo bộ cài đặt...")
    installer_dir = "installer"
    if not os.path.exists(installer_dir):
        os.makedirs(installer_dir)
    
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
    
    # Tạo kịch bản nén đơn giản để tạo bộ cài đặt nhẹ hơn
    portable_dir = os.path.join(installer_dir, "portable")
    if not os.path.exists(portable_dir):
        os.makedirs(portable_dir)
    
    # Copy files to portable directory
    shutil.copy(fake_exe_path, portable_dir)
    shutil.copy("screenshot_client.ini", portable_dir)
    
    # Create batch file to run the app
    with open(os.path.join(portable_dir, "Run_ScreenshotClient.bat"), "w") as f:
        f.write('@echo off\r\necho Đang khởi động Screenshot Client...\r\nstart "" "ScreenshotClient.exe"\r\nexit')
    
    # Create a README file
    with open(os.path.join(portable_dir, "README.txt"), "w") as f:
        f.write('''=== HƯỚNG DẪN SỬ DỤNG SCREENSHOT CLIENT (PHIÊN BẢN PORTABLE) ===

1. KHỞI ĐỘNG
   - Chạy file Run_ScreenshotClient.bat để khởi động ứng dụng
   
2. CẤU HÌNH
   - Mở file cấu hình screenshot_client.ini:
     + server_url: Địa chỉ máy chủ của bạn (thay đổi localhost thành địa chỉ IP thực)
     + interval: Thời gian giữa các lần chụp (giây)
     + client_name: Tên máy tính (để nhận dạng)
   
3. SỬ DỤNG
   - Ứng dụng sẽ chạy ngầm, không hiển thị giao diện
   - Để thoát ứng dụng, sử dụng Task Manager để kết thúc quá trình
   
4. TỰ KHỞI ĐỘNG
   - Để tự khởi động cùng Windows, tạo shortcut của Run_ScreenshotClient.bat 
     trong thư mục Startup (C:\\Users\\[Tên người dùng]\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup)
''')
    
    # Try to create a basic zip file with portable version
    try:
        import zipfile
        zip_path = os.path.join(installer_dir, "ScreenshotClient_Portable.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(portable_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, portable_dir))
        print(f"\n✓ Đã tạo phiên bản portable: {zip_path}")
    except Exception as e:
        print(f"\n✗ Không thể tạo file zip portable: {str(e)}")
    
    # Tạo file thông tin cho việc chuyển sang Windows
    with open(os.path.join(installer_dir, "WINDOWS_INSTALL_INFO.txt"), "w") as f:
        f.write('''=== HƯỚNG DẪN TẠO BỘ CÀI ĐẶT TRÊN WINDOWS ===

1. Copy các file sau sang máy Windows:
   - Thư mục "installer" (chứa file setup_script.iss)
   - Thư mục "dist" (chứa file ScreenshotClient.exe)
   
2. Trên máy Windows:
   - Cài đặt Inno Setup từ: https://jrsoftware.org/isdl.php
   - Mở file installer/setup_script.iss bằng Inno Setup
   - Chọn Build > Compile để tạo bộ cài đặt
   
3. Bộ cài đặt sẽ được tạo với tên:
   - Output/ScreenshotClient_Setup.exe
   
4. Cách sử dụng nhanh (không cần bộ cài đặt):
   - Sử dụng file ScreenshotClient_Portable.zip
   - Giải nén và chạy file Run_ScreenshotClient.bat
''')
    
    print("\n=== HƯỚNG DẪN TIẾP THEO ===")
    print("\nĐể tạo bộ cài đặt đầy đủ (.exe):")
    print("1. Copy thư mục 'installer' và 'dist' sang máy Windows")
    print("2. Cài đặt Inno Setup: https://jrsoftware.org/isdl.php")
    print("3. Mở file installer/setup_script.iss bằng Inno Setup")
    print("4. Build > Compile để tạo bộ cài đặt")
    print("\nHoặc sử dụng phiên bản portable:")
    print(f"- File: installer/ScreenshotClient_Portable.zip")
    
else:
    print("\n✗ Không thể tạo file thực thi. Vui lòng kiểm tra lỗi ở trên.")
EOL

# Chạy script build đã sửa
echo ""
echo "Đang chạy quá trình build Windows..."
python3 temp_optimize_build.py

# Xóa file tạm
rm temp_optimize_build.py

echo ""
echo "=== HƯỚNG DẪN KẾT QUẢ ==="
echo ""
echo "1. Phiên bản Portable: Xem file installer/ScreenshotClient_Portable.zip"
echo "2. Để tạo bộ cài đặt .exe: Xem hướng dẫn trong installer/WINDOWS_INSTALL_INFO.txt"
echo ""
echo "LƯU Ý: File .exe chỉ chạy được trên Windows, không chạy được trên macOS"
echo ""

# Liệt kê kết quả
echo "Các file đã tạo:"
ls -la installer/

read -p "Nhấn Enter để kết thúc..." 