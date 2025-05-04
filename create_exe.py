"""
Script để tạo file thực thi (.exe) cho ứng dụng screenshot_client
Sử dụng PyInstaller để đóng gói

Hướng dẫn sử dụng:
1. Cài đặt PyInstaller: pip install pyinstaller
2. Chạy script này: python create_exe.py
3. File .exe sẽ được tạo trong thư mục 'dist'
"""

import os
import shutil
import subprocess
import sys

def create_exe():
    print("Bắt đầu tạo file .exe cho screenshot_client...")
    
    # Cài đặt các package cần thiết
    print("Đang cài đặt các package cần thiết...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "pyautogui", "pillow"])
    
    # Tạo file .exe
    print("Đang tạo file .exe...")
    subprocess.check_call([
        "pyinstaller",
        "--onefile",
        "--name", "ScreenshotClient",
        "--add-data", "screenshot_client.ini:.",
        "screenshot_client.py"
    ])
    
    print("\nĐã tạo xong file .exe!")
    print("File .exe nằm trong thư mục 'dist'")
    print("\nHướng dẫn sử dụng:")
    print("1. Copy thư mục 'dist' lên máy client")
    print("2. Chạy file ScreenshotClient.exe")
    print("3. Chương trình sẽ tự động tạo file cấu hình nếu chưa có")
    print("4. Chỉnh sửa file screenshot_client.ini để cập nhật địa chỉ server")

if __name__ == "__main__":
    create_exe() 