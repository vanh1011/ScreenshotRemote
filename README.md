# HỆ THỐNG THEO DÕI MÀN HÌNH TỪ XA (SCREENSHOT MONITORING SYSTEM)

Hệ thống theo dõi màn hình cho phép quản lý và giám sát nhiều máy tính từ xa thông qua chụp màn hình định kỳ.

## 1. TỔNG QUAN HỆ THỐNG

### 1.1 Thành phần chính

Hệ thống gồm hai phần chính:

- **Screenshot Server**: Máy chủ PHP nhận và lưu trữ ảnh chụp màn hình
- **Screenshot Client**: Ứng dụng Python chạy trên máy người dùng, tự động chụp và gửi ảnh lên server

### 1.2 Yêu cầu hệ thống

#### Server
- PHP 7.0+ với extension GD
- Apache/Nginx
- XAMPP/WAMP/LAMP (cho môi trường phát triển)

#### Client
- Python 3.6+ 
- Thư viện: pyautogui, requests, pillow

## 2. CÀI ĐẶT SERVER

### 2.1 Sử dụng XAMPP (Phát triển)

1. Cài đặt XAMPP từ [trang chủ](https://www.apachefriends.org/)
2. Giải nén thư mục `screenshot_server` vào `htdocs`
3. Khởi động Apache từ XAMPP Control Panel
4. Truy cập: http://localhost/screenshot_server/

### 2.2 Cài đặt trên hosting (Triển khai)

1. Upload toàn bộ thư mục `screenshot_server` lên hosting
2. Đảm bảo PHP version tương thích
3. Cấp quyền ghi cho thư mục `uploads` và `logs`: `chmod 755 uploads logs`

### 2.3 Cấu trúc thư mục server

```
screenshot_server/
├── config.php          # Cấu hình server
├── index.php           # Trang quản lý chính
├── upload.php          # API nhận ảnh từ client
├── verify.php          # Kiểm tra kết nối
├── delete_all.php      # Xóa toàn bộ ảnh
├── css/                # Style sheets
├── js/                 # JavaScript
├── uploads/            # Thư mục chứa ảnh
└── logs/               # Nhật ký hoạt động
```

## 3. CÀI ĐẶT CLIENT

### 3.1 Cài đặt thủ công

1. Cài đặt Python 3.6+
2. Cài đặt các thư viện cần thiết:
   ```
   pip install pyautogui requests pillow
   ```
3. Tải và giải nén source code
4. Sửa file `screenshot_client.ini` để cấu hình:
   - `server_url`: URL của máy chủ (VD: http://192.168.1.100/screenshot_server/upload.php)
   - `interval`: Thời gian giữa các lần chụp (giây)
   - `client_name`: Tên máy tính

5. Chạy client:
   ```
   python screenshot_client.py
   ```

### 3.2 Cài đặt tự động

#### Windows:
1. Tải file `ScreenshotClient_Setup.exe`
2. Chạy file cài đặt và làm theo hướng dẫn
3. Ứng dụng sẽ tự động khởi động sau khi cài đặt

#### macOS:
1. Tải file `ScreenshotClient.app` hoặc file cài đặt `.pkg`
2. Chạy file `install.sh` hoặc mở file `.pkg`
3. Ứng dụng sẽ tự động khởi động

#### Linux:
1. Tải file `install.sh`
2. Cấp quyền thực thi: `chmod +x install.sh`
3. Chạy file: `./install.sh`

### 3.3 Phiên bản Portable (không cần cài đặt)
1. Tải file `ScreenshotClient_Portable.zip`
2. Giải nén vào thư mục tùy chọn
3. Chạy file `Run_ScreenshotClient.bat` (Windows)

## 4. SỬ DỤNG HỆ THỐNG

### 4.1 Quản lý server

1. Truy cập địa chỉ server (VD: http://localhost/screenshot_server/)
2. Xem danh sách máy tính đang kết nối
3. Xem ảnh chụp màn hình mới nhất của từng máy
4. Xóa ảnh cũ nếu cần

### 4.2 Cấu hình client

Mở file `screenshot_client.ini` để chỉnh sửa:

```ini
[SERVER]
server_url = http://192.168.1.100/screenshot_server/upload.php
interval = 60

[CLIENT]
client_id = abc123
client_name = Computer_Name
```

## 5. TẠO BỘ CÀI ĐẶT RIÊNG

### 5.1 Build cho Windows

1. Cài đặt các công cụ cần thiết:
   ```
   pip install pyinstaller
   ```
   
2. Chạy script build tự động:
   ```
   build_client.bat
   ```
   
   hoặc build thủ công:
   ```
   pyinstaller --onefile --noconsole --name=ScreenshotClient --add-data="screenshot_client.ini;." screenshot_client.py
   ```

3. Tạo bộ cài đặt với Inno Setup:
   - Cài đặt [Inno Setup](https://jrsoftware.org/isdl.php)
   - Mở file `installer/setup_script.iss`
   - Build > Compile
   
### 5.2 Build cho macOS

1. Cài đặt các công cụ cần thiết:
   ```
   pip install pyinstaller
   ```

2. Chạy script build tự động:
   ```
   ./build_client.sh
   ```
   
   hoặc build thủ công:
   ```
   pyinstaller --onefile --windowed --name=ScreenshotClient --add-data="screenshot_client.ini:." screenshot_client.py
   ```

3. Tạo file cài đặt `.pkg` (tùy chọn):
   - Cài đặt [Packages](http://s.sudre.free.fr/Software/Packages/about.html)
   - Tạo mới project và thêm app từ thư mục `dist/`

### 5.3 Build cho Linux

1. Cài đặt các công cụ cần thiết:
   ```
   pip install pyinstaller
   ```
   
2. Chạy script build tự động:
   ```
   ./build_client.sh
   ```
   
   hoặc build thủ công:
   ```
   pyinstaller --onefile --name=ScreenshotClient --add-data="screenshot_client.ini:." screenshot_client.py
   ```

## 6. KHẮC PHỤC SỰ CỐ

| Vấn đề | Giải pháp |
|--------|-----------|
| Client không kết nối được server | - Kiểm tra URL server trong file cấu hình<br>- Đảm bảo server đang chạy<br>- Kiểm tra kết nối mạng (ping) |
| Server không nhận được ảnh | - Kiểm tra quyền ghi vào thư mục uploads<br>- Kiểm tra log PHP trên server |
| Báo lỗi thư viện | - Cài đặt lại các thư viện Python cần thiết |
| Chất lượng ảnh kém | - Điều chỉnh trong file config.php trên server |

## 7. THÔNG TIN BỔ SUNG

### 7.1 Bảo mật

- Hệ thống hiện tại không có xác thực người dùng
- Nên triển khai trong mạng nội bộ hoặc thêm xác thực trước khi dùng trên internet
- Cân nhắc mã hóa dữ liệu trước khi gửi đi

### 7.2 Khả năng mở rộng

- Thêm tính năng quản lý người dùng
- Thêm tính năng theo dõi theo thời gian thực
- Tích hợp lưu trữ đám mây

---

## LIÊN HỆ VÀ HỖ TRỢ

Nếu bạn có câu hỏi hoặc cần hỗ trợ, vui lòng liên hệ qua email: example@example.com