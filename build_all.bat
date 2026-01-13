@echo off
REM Build script cho Windows - Tạo installer hoàn chỉnh

echo ============================================================
echo   CAPSCREEN - BUILD INSTALLER
echo ============================================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat!
    echo Tai tai: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Kiem tra dependencies...
pip install pyinstaller flask pyautogui requests pillow pynput

echo.
echo [2/4] Build client exe...
cd client
python build.py
if errorlevel 1 (
    echo [ERROR] Build client that bai!
    pause
    exit /b 1
)
cd ..

echo.
echo [3/4] Kiem tra Inno Setup...
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo [WARNING] Inno Setup chua duoc cai dat!
    echo Tai tai: https://jrsoftware.org/isdl.php
    echo.
    echo Ban co the build installer thu cong:
    echo 1. Cai Inno Setup
    echo 2. Mo installer/setup.iss
    echo 3. Build -^> Compile
    pause
    exit /b 0
)

echo.
echo [4/4] Build installer...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\setup.iss

echo.
echo ============================================================
echo   BUILD HOAN THANH!
echo ============================================================
echo.
echo Output files:
echo   - client\dist\CapScreenClient.exe
echo   - installer\CapScreen-Client-Setup.exe
echo.
echo Phan phoi file installer cho users!
echo ============================================================
pause
