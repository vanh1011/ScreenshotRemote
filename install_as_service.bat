@echo off
echo Cài đặt ScreenshotClient như một dịch vụ Windows...
sc create ScreenshotService binPath= "%~dp0dist\ScreenshotClient.exe" DisplayName= "Screenshot Client Service" start= auto
sc description ScreenshotService "Dịch vụ chụp màn hình tự động và gửi về máy chủ"
echo Đã cài đặt dịch vụ thành công!
echo Dịch vụ sẽ tự động khởi động khi máy tính khởi động
echo Để khởi động dịch vụ ngay, gõ: sc start ScreenshotService
pause
