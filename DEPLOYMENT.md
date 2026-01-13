# 🚀 HƯỚNG DẪN TRIỂN KHAI - A → Z

---

## 📌 BẠN CẦN GÌ?

- 1 máy **Server** (Windows/Mac) - nhận ảnh
- N máy **Client** (Windows) - gửi ảnh
- Tất cả cùng WiFi
- Thư mục `capScreen` (code đã nhận)

---

## 🖥️ BƯỚC 1: SETUP SERVER (1 MÁY WINDOWS)

> Server là máy nhận và hiển thị ảnh từ các máy client

---

### **1.1. Cài Python**

1. Mở trình duyệt, vào: **https://www.python.org/downloads/**
2. Click nút vàng **"Download Python 3.x"**
3. Sau khi tải xong, **double click** file (VD: `python-3.12.0-amd64.exe`)
4. **QUAN TRỌNG:** ✅ Tích vào ô **"Add python.exe to PATH"** (ở dưới cùng)
5. Click **"Install Now"**
6. Đợi cài xong (1-2 phút)
7. Click **"Close"**

**Kiểm tra đã cài thành công:**
1. Nhấn phím **Windows + R**
2. Gõ: `cmd` → Enter
3. Trong cửa sổ đen, gõ: `python --version` → Enter
4. Thấy hiện `Python 3.x.x` = **Thành công!** ✅
5. Đóng cửa sổ CMD

---

### **1.2. Cài Flask**

1. Nhấn **Windows + R**
2. Gõ: `cmd` → Enter
3. Gõ lệnh sau rồi Enter:
   ```
   pip install flask
   ```
4. Đợi cài xong (thấy chữ "Successfully installed flask")
5. Đóng cửa sổ CMD

---

### **1.3. Chạy Server**

1. Mở **File Explorer** (Windows + E)
2. Tìm thư mục `capScreen` (thư mục bạn nhận được)
3. Vào thư mục `server` (double click)
4. **Shift + Chuột phải** vào khoảng trống → Chọn **"Mở cửa sổ PowerShell tại đây"**
   - Nếu không thấy option này → Chọn **"Mở trong Terminal"**
5. Trong cửa sổ PowerShell/Terminal, gõ:
   ```
   python app.py
   ```
6. Nhấn Enter

---

### **1.4. Kiểm tra Server**

**Sau khi chạy lệnh `python app.py`, bạn sẽ thấy:**
```
============================================================
🚀 CapScreen Server Starting...
============================================================
📍 Server URL: http://localhost:8080
📁 Upload folder: C:\...\capScreen\server\uploads
============================================================
🌐 Opening browser...
```

- ✅ Browser tự động mở, hiển thị **Dashboard**
- ✅ Thấy trang web trống (chưa có ảnh - bình thường)

---

### **1.5. Tìm địa chỉ IP Server**

> **Quan trọng:** Cần IP này để cấu hình client

1. **Để cửa sổ PowerShell chạy server** (không tắt)
2. Mở cửa sổ CMD mới: **Windows + R** → Gõ `cmd` → Enter
3. Gõ lệnh:
   ```
   ipconfig
   ```
4. Tìm dòng **"IPv4 Address"** (thường có dạng `192.168.x.x`)
5. **GHI NHỚ SỐ NÀY!** (VD: `192.168.1.100`)

**Ví dụ:**
```
Ethernet adapter Ethernet:
   IPv4 Address. . . . . . . . . . . : 192.168.1.100  ← ĐÂY!
```

---

## � BƯỚC 2: BUILD INSTALLER (CHỈ LÀM 1 LẦN)

> **Dành cho:** Người có code và muốn tạo file installer để gửi cho users

---

### **2.1. Cài PyInstaller**

1. Nhấn **Windows + R**
2. Gõ: `cmd` → Enter
3. Gõ lệnh:
   ```
   pip install pyinstaller
   ```
4. Đợi cài xong (1-2 phút)
5. Đóng CMD

---

### **2.2. Cài Inno Setup**

1. Mở trình duyệt, vào: **https://jrsoftware.org/isdl.php**
2. Click link **"Download Inno Setup"** (file `.exe`, khoảng 5MB)
3. Sau khi tải xong, **double click** file `innosetup-6.x.x.exe`
4. Click **Next** → **Next** → **Install**
5. Đợi cài xong
6. Click **Finish**

---

### **2.3. Build Installer**

1. Mở **File Explorer** (Windows + E)
2. Tìm thư mục `capScreen`
3. **Double click** file `build_all.bat`
4. Cửa sổ CMD sẽ mở, chạy tự động
5. Đợi 3-5 phút (sẽ thấy nhiều dòng chữ chạy)
6. Khi thấy "BUILD HOÀN THÀNH!" → **Xong!**

**Output:**
- File `installer/CapScreen-Client-Setup.exe` ⭐ (đây là file gửi cho users)

---

### **2.4. Kiểm tra file đã build**

1. Vào thư mục `capScreen/installer`
2. Thấy file `CapScreen-Client-Setup.exe` (khoảng 50-100 MB)
3. ✅ Đây là file installer hoàn chỉnh!

---

## 📦 BƯỚC 3: CÀI CLIENT (TỪNG MÁY)

### **3.1. Chạy Installer**

1. Double click `CapScreen-Client-Setup.exe`
2. Next

---

### **3.2. Nhập thông tin**

**Server URL:**
```
http://192.168.x.x:8080/api/upload
(Thay x.x bằng IP server ở Bước 1.3)
```

**Client Name:**
```
PC-Ke-Toan
(Hoặc tên bất kỳ)
```

---

### **3.3. Install**

1. Next → Install
2. Đợi 30 giây
3. ✅ Tích "Launch CapScreen Client"
4. Finish

---

### **3.4. Kiểm tra**

1. Nhấn bất kỳ phím nào
2. Mở browser: `http://192.168.x.x:8080`
3. Thấy ảnh vừa chụp! ✅

---

## ✅ XONG!

**Client đã:**
- Tự động chạy khi Windows khởi động
- Chụp màn hình khi gõ phím
- Gửi về server

**Lặp lại Bước 3 cho từng máy cần giám sát.**

---

## 🐛 LỖI THƯỜNG GẶP

### **Client không kết nối Server:**
1. Kiểm tra Server đang chạy
2. Ping server: `ping 192.168.x.x`
3. Kiểm tra Firewall (cho phép port 8080)

### **Không thấy ảnh trên Dashboard:**
1. Nhấn phím để chụp
2. Đợi 5 giây (cooldown)
3. Refresh browser

---

**Version:** 1.0
