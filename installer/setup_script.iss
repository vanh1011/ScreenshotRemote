
[Setup]
AppName=Screenshot Client
AppVersion=1.0
DefaultDirName={commonpf}\Screenshot Client
DefaultGroupName=Screenshot Client
OutputBaseFilename=ScreenshotClient_Setup
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "dist\ScreenshotClient.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "screenshot_client.ini"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist

[Icons]
Name: "{group}\Screenshot Client"; Filename: "{app}\ScreenshotClient.exe"
Name: "{commondesktop}\Screenshot Client"; Filename: "{app}\ScreenshotClient.exe"
Name: "{group}\Thay đổi cấu hình"; Filename: "{app}\screenshot_client.ini"; IconFilename: "{sys}\shell32.dll"; IconIndex=71

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "ScreenshotClient"; ValueData: """{app}\ScreenshotClient.exe"""; Flags: uninsdeletevalue

[Run]
Filename: "{app}\ScreenshotClient.exe"; Description: "Chạy ứng dụng sau khi cài đặt"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "taskkill"; Parameters: "/f /im ScreenshotClient.exe"; Flags: runhidden
