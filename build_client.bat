@echo off
echo === SCREENSHOT CLIENT BUILDER ===
echo.
echo Quá trình này sẽ tạo file cài đặt cho Screenshot Client
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python không được cài đặt hoặc không có trong PATH
    echo Vui lòng cài đặt Python 3.6+ và thêm vào PATH
    pause
    exit /b 1
)

echo [✓] Đã tìm thấy Python

REM Cài đặt các thư viện cần thiết
echo.
echo Đang cài đặt các thư viện cần thiết...
python -m pip install -q pyinstaller requests pyautogui pillow
echo [✓] Đã cài đặt các thư viện cần thiết

REM Chạy script build
echo.
echo Đang chạy quá trình build...
python optimize_build.py

echo.
echo === TIẾP THEO ===
echo.
echo 1. Cài đặt Inno Setup từ: https://jrsoftware.org/isdl.php
echo 2. Mở file installer/setup_script.iss bằng Inno Setup
echo 3. Nhấn Build ^> Compile để tạo bộ cài đặt
echo.
echo Bộ cài đặt sẽ được tạo trong thư mục Output/ScreenshotClient_Setup.exe
echo.

pause 