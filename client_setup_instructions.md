# Hướng dẫn cài đặt Screenshot Client

Phần mềm Screenshot Client giúp chụp ảnh màn hình tự động và gửi về máy chủ trung tâm. Dưới đây là các cách cài đặt đơn giản cho người dùng cuối.

## Cài đặt trên Windows

### Cách 1: Sử dụng file cài đặt tự động (Khuyên dùng)

1. Tải file `ScreenshotClient_Setup.zip` từ máy chủ
2. Giải nén và mở thư mục
3. Nhấp chuột phải vào file `setup_client.bat` và chọn "Run as administrator"
4. Làm theo các bước trên màn hình:
   - Nhập địa chỉ IP của máy chủ
   - Đặt thời gian chụp màn hình (mặc định 60 giây)
   - Nhập tên máy tính (hiển thị trên server)
   - Chọn có/không cài đặt như dịch vụ Windows
   - Chọn có/không chạy ngay

### Cách 2: Chạy file thực thi trực tiếp

1. Tải file `ScreenshotClient.exe` từ máy chủ
2. Đặt file vào thư mục bạn muốn cài đặt (ví dụ: `C:\ScreenshotClient`)
3. Tạo file `screenshot_client.ini` trong cùng thư mục với nội dung:
   ```
   [SERVER]
   server_url = http://192.168.0.123/screenshot_server/upload.php
   interval = 60
   
   [CLIENT]
   client_id = auto_generated
   client_name = TenMayTinh
   ```
4. Thay đổi `192.168.0.123` thành địa chỉ IP của máy chủ
5. Chạy file `ScreenshotClient.exe`

## Cài đặt trên macOS

1. Tải file `setup_client.sh` từ máy chủ
2. Mở Terminal, di chuyển đến thư mục chứa file vừa tải về:
   ```
   cd ~/Downloads
   ```
3. Cấp quyền thực thi cho file:
   ```
   chmod +x setup_client.sh
   ```
4. Chạy script với quyền admin:
   ```
   sudo ./setup_client.sh
   ```
5. Làm theo các bước trên màn hình:
   - Nhập địa chỉ IP của máy chủ
   - Đặt thời gian chụp màn hình (mặc định 60 giây)
   - Nhập tên máy tính (hiển thị trên server)
   - Chọn có/không bật tự động khi đăng nhập
   - Chọn có/không chạy ngay

## Cài đặt trên Linux

Tương tự như macOS, sử dụng file `setup_client.sh`:

1. Tải file `setup_client.sh` từ máy chủ
2. Mở Terminal, di chuyển đến thư mục chứa file:
   ```
   cd ~/Downloads
   ```
3. Cấp quyền thực thi:
   ```
   chmod +x setup_client.sh
   ```
4. Chạy script với quyền root:
   ```
   sudo ./setup_client.sh
   ```
5. Làm theo các bước trên màn hình

## Kiểm tra hoạt động

Sau khi cài đặt, bạn có thể kiểm tra phần mềm đã hoạt động chưa:

1. Truy cập vào trang quản lý từ máy chủ:
   ```
   http://địa_chỉ_IP_máy_chủ/screenshot_server/
   ```
2. Nếu cài đặt thành công, bạn sẽ thấy tên máy tính và ảnh chụp màn hình mới nhất xuất hiện

## Gỡ cài đặt

### Windows

1. Dừng dịch vụ (nếu đã cài đặt): 
   ```
   sc stop ScreenshotService
   sc delete ScreenshotService
   ```
2. Xóa thư mục cài đặt (mặc định là `C:\ScreenshotClient`)
3. Xóa shortcut trong thư mục Startup (nếu có)

### macOS / Linux

1. Dừng dịch vụ:
   - macOS: `launchctl unload ~/Library/LaunchAgents/com.screenshot.client.plist`
   - Linux: `sudo systemctl stop screenshot-client && sudo systemctl disable screenshot-client`
2. Xóa thư mục cài đặt:
   - macOS: `/Applications/ScreenshotClient`
   - Linux: `/opt/screenshot-client`
3. Xóa file dịch vụ:
   - macOS: `~/Library/LaunchAgents/com.screenshot.client.plist`
   - Linux: `/etc/systemd/system/screenshot-client.service` 