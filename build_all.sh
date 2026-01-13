#!/bin/bash

# Build script cho macOS/Linux (chỉ build client, không có installer)

echo "============================================================"
echo "  CAPSCREEN - BUILD CLIENT"
echo "============================================================"
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 chưa được cài đặt!"
    exit 1
fi

echo "[1/2] Kiểm tra dependencies..."
pip3 install pyinstaller flask pyautogui requests pillow pynput

echo ""
echo "[2/2] Build client..."
cd client
python3 build.py

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "  BUILD HOÀN THÀNH!"
    echo "============================================================"
    echo ""
    echo "Output: client/dist/CapScreenClient"
    echo ""
    echo "Chạy: ./client/dist/CapScreenClient"
    echo "============================================================"
else
    echo "[ERROR] Build thất bại!"
    exit 1
fi
