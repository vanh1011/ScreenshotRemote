"""
Script đóng gói tất cả các file thành gói cài đặt cho client và server
"""

import os
import shutil
import zipfile
import platform
import subprocess

def create_client_package():
    """Tạo gói cài đặt cho client"""
    print("Đang tạo gói cài đặt cho client...")
    
    # Tạo thư mục build nếu chưa có
    if not os.path.exists("build"):
        os.makedirs("build")
        
    # Tạo thư mục client
    client_dir = os.path.join("build", "client")
    if os.path.exists(client_dir):
        shutil.rmtree(client_dir)
    os.makedirs(client_dir)
    
    # Copy các file client
    files_to_copy = [
        "screenshot_client.py",
        "screenshot_client.ini",
        "setup_client.bat",
        "setup_client.sh",
        "requirements.txt",
        "client_setup_instructions.md"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy(file, client_dir)
    
    # Nếu có PyInstaller, tạo file thực thi
    try:
        import PyInstaller
        print("Đang tạo file thực thi...")
        
        # Lưu thư mục hiện tại
        current_dir = os.getcwd()
        
        # Di chuyển đến thư mục client
        os.chdir(client_dir)
        
        # Tạo file exe
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--add-data", "screenshot_client.ini;.",
            "--name", "ScreenshotClient",
            "screenshot_client.py"
        ]
        
        subprocess.call(cmd)
        
        # Di chuyển file exe từ thư mục dist vào thư mục client
        if os.path.exists(os.path.join("dist", "ScreenshotClient.exe")):
            shutil.copy(os.path.join("dist", "ScreenshotClient.exe"), ".")
            
        # Trở về thư mục ban đầu
        os.chdir(current_dir)
        
    except ImportError:
        print("PyInstaller không được cài đặt. Bỏ qua việc tạo file thực thi.")
    
    # Tạo file zip
    client_zip = os.path.join("build", "ScreenshotClient_Setup.zip")
    with zipfile.ZipFile(client_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(client_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, client_dir))
    
    print(f"Đã tạo gói cài đặt client: {client_zip}")

def create_server_package():
    """Tạo gói cài đặt cho server"""
    print("Đang tạo gói cài đặt cho server...")
    
    # Tạo thư mục build nếu chưa có
    if not os.path.exists("build"):
        os.makedirs("build")
        
    # Tạo thư mục server
    server_dir = os.path.join("build", "screenshot_server")
    if os.path.exists(server_dir):
        shutil.rmtree(server_dir)
    os.makedirs(server_dir)
    os.makedirs(os.path.join(server_dir, "uploads"))
    
    # Copy các file server
    files_to_copy = [
        "index.php",
        "upload.php",
        "client_images.php",
        "delete_image.php",
        "cleanup_old_images.php",
        "README.md"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy(file, server_dir)
    
    # Tạo file zip
    server_zip = os.path.join("build", "ScreenshotServer_Setup.zip")
    with zipfile.ZipFile(server_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(server_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, os.path.dirname(server_dir)))
    
    print(f"Đã tạo gói cài đặt server: {server_zip}")

def create_all_packages():
    """Tạo tất cả các gói cài đặt"""
    create_client_package()
    create_server_package()
    
    print("\nĐã tạo xong tất cả các gói cài đặt!")
    print("Các gói cài đặt được lưu trong thư mục 'build'.")
    
    # Hướng dẫn cài đặt
    print("\nHướng dẫn cài đặt:")
    print("1. Server:")
    print("   - Giải nén file ScreenshotServer_Setup.zip")
    print("   - Copy thư mục screenshot_server vào thư mục htdocs của XAMPP")
    print("   - Truy cập http://localhost/screenshot_server/ để kiểm tra")
    print("2. Client Windows:")
    print("   - Giải nén file ScreenshotClient_Setup.zip")
    print("   - Chạy file setup_client.bat với quyền Administrator")
    print("3. Client macOS/Linux:")
    print("   - Giải nén file ScreenshotClient_Setup.zip")
    print("   - Chạy lệnh: sudo ./setup_client.sh")

if __name__ == "__main__":
    create_all_packages() 