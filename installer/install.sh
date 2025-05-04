#!/bin/bash
# Script cài đặt Screenshot Client

# Tạo thư mục ứng dụng
mkdir -p ~/Applications/ScreenshotClient

# Copy file
cp -R ScreenshotClient.app ~/Applications/
cp screenshot_client.ini ~/Applications/ScreenshotClient/

# Tạo file khởi động tự động
mkdir -p ~/Library/LaunchAgents
cat > ~/Library/LaunchAgents/com.example.screenshotclient.plist << 'EOL'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.screenshotclient</string>
    <key>ProgramArguments</key>
    <array>
        <string>~/Applications/ScreenshotClient.app/Contents/MacOS/ScreenshotClient</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOL

# Tải ứng dụng
launchctl load ~/Library/LaunchAgents/com.example.screenshotclient.plist

echo "Đã cài đặt Screenshot Client thành công!"
