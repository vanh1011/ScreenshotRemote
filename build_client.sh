#!/bin/bash

echo "=== SCREENSHOT CLIENT BUILDER ==="
echo ""
echo "Quá trình này sẽ tạo file cài đặt cho Screenshot Client"
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "[X] Python không được cài đặt hoặc không có trong PATH"
    echo "Vui lòng cài đặt Python 3.6+ và thêm vào PATH"
    exit 1
fi

echo "[✓] Đã tìm thấy Python"

# Cài đặt các thư viện cần thiết
echo ""
echo "Đang cài đặt các thư viện cần thiết..."
python3 -m pip install -q pyinstaller requests pyautogui pillow
echo "[✓] Đã cài đặt các thư viện cần thiết"

# Chạy script build
echo ""
echo "Đang chạy quá trình build..."
python3 optimize_build.py

echo ""
echo "=== TIẾP THEO ==="
echo ""
echo "Để tạo bộ cài đặt cho macOS:"
echo "1. Cài đặt Packages từ: http://s.sudre.free.fr/Software/Packages/about.html"
echo "2. Tạo package project mới (File > New)"
echo "3. Thêm app từ thư mục dist/"
echo ""
echo "Bộ cài đặt sẽ được tạo theo hướng dẫn của Packages"
echo ""

read -p "Nhấn Enter để kết thúc..." 