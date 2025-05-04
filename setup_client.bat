@echo off
echo ===============================
echo Cài đặt Screenshot Client
echo ===============================
echo.

:: Kiểm tra quyền admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Vui lòng chạy chương trình này với quyền Administrator!
    echo Nhấn chuột phải vào file và chọn "Run as administrator"
    pause
    exit /b
)

:: Tạo thư mục cài đặt
set INSTALL_DIR=C:\ScreenshotClient
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Sao chép các file
echo Đang sao chép các file cần thiết...
copy /Y "ScreenshotClient.exe" "%INSTALL_DIR%\"
copy /Y "screenshot_client.ini" "%INSTALL_DIR%\"

:: Cấu hình client
echo.
echo ====== CẤU HÌNH CLIENT ======
set /p SERVER_IP=Nhập địa chỉ IP của máy chủ (ví dụ: 192.168.0.123): 
set /p INTERVAL=Nhập thời gian chụp màn hình (giây, mặc định 60): 
if "%INTERVAL%"=="" set INTERVAL=60

set /p CLIENT_NAME=Nhập tên máy tính (hiển thị trên server): 
if "%CLIENT_NAME%"=="" set CLIENT_NAME=%COMPUTERNAME%

:: Tạo file cấu hình
echo Đang tạo file cấu hình...
echo [SERVER] > "%INSTALL_DIR%\screenshot_client.ini"
echo server_url = http://%SERVER_IP%/screenshot_server/upload.php >> "%INSTALL_DIR%\screenshot_client.ini"
echo interval = %INTERVAL% >> "%INSTALL_DIR%\screenshot_client.ini"
echo. >> "%INSTALL_DIR%\screenshot_client.ini"
echo [CLIENT] >> "%INSTALL_DIR%\screenshot_client.ini"
echo client_id = auto_generated >> "%INSTALL_DIR%\screenshot_client.ini"
echo client_name = %CLIENT_NAME% >> "%INSTALL_DIR%\screenshot_client.ini"

:: Tạo shortcut
echo Đang tạo shortcut khởi động cùng Windows...
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SHORTCUT_PATH=%STARTUP_FOLDER%\ScreenshotClient.lnk

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%INSTALL_DIR%\ScreenshotClient.exe'; $Shortcut.Save()"

:: Tạo file bat để chạy
echo @echo off > "%INSTALL_DIR%\run_client.bat"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\run_client.bat"
echo start ScreenshotClient.exe >> "%INSTALL_DIR%\run_client.bat"
echo exit >> "%INSTALL_DIR%\run_client.bat"

:: Hỏi người dùng có muốn cài đặt như dịch vụ không
echo.
set /p INSTALL_SERVICE=Bạn có muốn cài đặt như dịch vụ Windows không? (Y/N): 
if /i "%INSTALL_SERVICE%"=="Y" (
    sc create ScreenshotService binPath= "%INSTALL_DIR%\ScreenshotClient.exe" DisplayName= "Screenshot Client Service" start= auto
    sc description ScreenshotService "Dịch vụ chụp màn hình tự động và gửi về máy chủ"
    sc start ScreenshotService
    echo Đã cài đặt và khởi động dịch vụ thành công!
) else (
    echo Không cài đặt dịch vụ. Chương trình sẽ tự khởi động khi đăng nhập Windows.
)

:: Hoàn tất
echo.
echo ====== CÀI ĐẶT HOÀN TẤT ======
echo Chương trình đã được cài đặt tại: %INSTALL_DIR%
echo Để chạy ngay, hãy mở file: %INSTALL_DIR%\run_client.bat
echo Chương trình sẽ tự động chạy khi khởi động Windows.
echo.

:: Hỏi người dùng có muốn chạy ngay không
set /p RUN_NOW=Bạn có muốn chạy chương trình ngay không? (Y/N): 
if /i "%RUN_NOW%"=="Y" (
    start "" "%INSTALL_DIR%\ScreenshotClient.exe"
    echo Đã khởi động chương trình!
)

echo.
echo Cảm ơn bạn đã cài đặt Screenshot Client!
pause 