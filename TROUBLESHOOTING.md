# 🛠️ Hướng dẫn xử lý lỗi thư mục bị hỏng (Corrupted Directory)

## 🔍 Mô tả lỗi

**Lỗi gốc:**
```
OSError: [WinError 1392] The file or directory is corrupted and unreadable
```

Lỗi này xảy ra khi:
- ❌ Thư mục client bị hỏng (corrupted)
- ❌ File system NTFS bị lỗi
- ❌ Bad sector trên ổ đĩa
- ❌ Tắt máy đột ngột khi đang ghi dữ liệu
- ❌ Virus/malware
- ❌ Lỗi phần cứng ổ đĩa

## ✅ Giải pháp đã áp dụng

### 1. **Error Handling trong Code**

Code đã được cập nhật để:
- ✅ Bắt lỗi `OSError` khi đọc thư mục bị hỏng
- ✅ Bỏ qua thư mục lỗi và tiếp tục xử lý các client khác
- ✅ Hiển thị cảnh báo trong console
- ✅ Dashboard vẫn hoạt động bình thường với các client còn lại

### 2. **Các vị trí đã được bảo vệ**

- ✅ `index()` - Dashboard chính
- ✅ `client_detail()` - Trang chi tiết client
- ✅ `migrate_files()` - Migration files cũ

## 🔧 Cách khắc phục thư mục bị hỏng

### **Phương án 1: Chạy CHKDSK (Khuyến nghị)**

1. Mở **Command Prompt** với quyền Administrator
2. Chạy lệnh:
   ```cmd
   chkdsk D: /F /R
   ```
   - `/F` - Sửa lỗi file system
   - `/R` - Tìm và khôi phục bad sectors
   - Thay `D:` bằng ổ đĩa chứa thư mục `uploads`

3. Nếu ổ đĩa đang được sử dụng, hệ thống sẽ hỏi có muốn chạy khi restart không → Chọn **Y**

4. Restart máy và đợi CHKDSK hoàn thành (có thể mất 30 phút - 2 giờ)

### **Phương án 2: Xóa thư mục bị hỏng**

Nếu CHKDSK không sửa được:

1. Mở **Command Prompt** với quyền Administrator
2. Xóa thư mục bị hỏng:
   ```cmd
   rd /s "D:\ScreenshotRemote-main\server\uploads\DESKTOP-BFHCV4P-2966"
   ```

3. Nếu lệnh trên không hoạt động, thử:
   ```cmd
   rmdir /s /q "\\?\D:\ScreenshotRemote-main\server\uploads\DESKTOP-BFHCV4P-2966"
   ```

### **Phương án 3: Sử dụng công cụ bên thứ 3**

Nếu cả 2 phương án trên đều thất bại:

1. **Unlocker** - Xóa file/folder bị khóa
2. **FileAssassin** - Xóa file cứng đầu
3. **CCleaner** - Dọn dẹp registry và file rác

## 📊 Kiểm tra log

Khi server chạy, nếu gặp thư mục bị hỏng, bạn sẽ thấy cảnh báo:

```
⚠️  WARNING: Cannot read client folder 'DESKTOP-BFHCV4P-2966': [WinError 1392] The file or directory is corrupted and unreadable
   Thư mục có thể bị hỏng. Hãy chạy CHKDSK hoặc xóa thư mục này.
```

## 🛡️ Phòng ngừa

Để tránh lỗi này trong tương lai:

1. ✅ **Tắt máy đúng cách** - Không tắt nguồn đột ngột
2. ✅ **Kiểm tra ổ đĩa định kỳ** - Chạy CHKDSK mỗi tháng
3. ✅ **Sử dụng UPS** - Tránh mất điện đột ngột
4. ✅ **Backup dữ liệu** - Sao lưu thư mục `uploads` thường xuyên
5. ✅ **Kiểm tra sức khỏe ổ đĩa** - Dùng CrystalDiskInfo để theo dõi

## 🔍 Kiểm tra sức khỏe ổ đĩa

Tải và cài đặt **CrystalDiskInfo**:
- Link: https://crystalmark.info/en/software/crystaldiskinfo/

Nếu thấy:
- ⚠️ **Caution** (Vàng) - Cần theo dõi
- ❌ **Bad** (Đỏ) - Cần thay ổ đĩa ngay

## 📞 Hỗ trợ

Nếu vẫn gặp vấn đề:
1. Kiểm tra log trong console
2. Chụp màn hình lỗi
3. Gửi thông tin chi tiết để được hỗ trợ
