# 📸 CapScreen - Hệ Thống Giám Sát Màn Hình

> Chụp màn hình khi gõ phím → Gửi về server → Xem trên web

---

## 🎯 DÀNH CHO AI?

- ✅ Quản lý muốn giám sát nhân viên (có đồng ý)
- ✅ IT muốn theo dõi nhiều máy từ xa
- ✅ Người cần backup màn hình tự động

---

## ⚡ HƯỚNG DẪN TRIỂN KHAI

### **Bạn nhận code và muốn triển khai?**
→ Đọc file **`DEPLOYMENT.md`** (hướng dẫn A→Z, 5 phút đọc)

### **Tóm tắt nhanh:**
1. **Server:** Cài Python + Flask → Chạy `python app.py`
2. **Build:** Chạy `build_all.bat` (Windows) → Nhận file installer
3. **Client:** Double click installer → Nhập IP server → Done!

---

## 📁 CẤU TRÚC

```
capScreen/
├── server/app.py           # Flask server
├── client/client.py        # Python client
├── client/config.json      # Cấu hình (IP server)
├── installer/setup.iss     # Inno Setup (Windows)
├── DEPLOYMENT.md           # ⭐ Hướng dẫn chi tiết
└── README.md               # File này
```

---

## 🚀 QUICK START (CHO DEV)

### **1. Server:**
```bash
pip install flask
cd server
python app.py
# → http://localhost:8080
```

### **2. Client:**
```bash
pip install pyautogui requests pillow pynput
cd client
# Sửa config.json với IP server
python client.py
# Nhấn phím → Chụp → Xem trên dashboard
```

---

## 🔧 CÔNG NGHỆ

- **Server:** Flask (Python)
- **Client:** Python + pynput + pyautogui
- **UI:** HTML/CSS (embedded)
- **Deploy:** PyInstaller + Inno Setup

---

## 📦 BUILD (WINDOWS)

```bash
# Client exe
cd client
python build.py

# Installer (cần Inno Setup)
# Mở installer/setup.iss → Compile
```

---

## 🌐 NETWORK

- **LAN:** Server IP = `192.168.x.x:8080`
- **Internet:** Dùng ngrok: `ngrok http 8080`

---

## 📖 TÀI LIỆU

- **DEPLOYMENT.md** - Hướng dẫn triển khai (cho người không biết code)
- **TROUBLESHOOTING.md** - Xử lý lỗi thường gặp (thư mục bị hỏng, etc.)
- **README.md** - File này (tổng quan)

---

## 🛠️ TROUBLESHOOTING

### **Lỗi: "The file or directory is corrupted and unreadable"**

Nếu gặp lỗi thư mục bị hỏng:

1. **Kiểm tra tự động:**
   ```bash
   cd server
   python check_corrupted_folders.py
   ```

2. **Xem hướng dẫn chi tiết:**
   - Đọc file `TROUBLESHOOTING.md`
   - Chạy CHKDSK để sửa lỗi ổ đĩa
   - Hoặc xóa thư mục bị hỏng

3. **Server vẫn hoạt động:**
   - Dashboard sẽ tự động bỏ qua thư mục lỗi
   - Các client khác vẫn hiển thị bình thường

---

## 📞 HỖ TRỢ

Email: kira10111907@gmail.com

---

**Version:** 1.0  
**License:** MIT
