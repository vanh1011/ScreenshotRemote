=== HƯỚNG DẪN SỬ DỤNG SCREENSHOT CLIENT (PHIÊN BẢN PORTABLE) ===

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
     trong thư mục Startup (C:\Users\[Tên người dùng]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup)
