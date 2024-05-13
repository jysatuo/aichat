# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = []
datas += collect_data_files('ntchat')


a = Analysis(
    ['C:\\Users\\jysatuo\\Desktop\\ai_assistant_tool\\main\\main.py'],
    pathex=['F:\\ProgramData\\Anaconda3\\Lib\\site-packages', 'F:\\ProgramData\\Anaconda3\\Lib\\site-packages\\PyQt5', 'F:\\ProgramData\\Anaconda3\\Lib\\site-packages\\tables', 'C:\\Users\\jysatuo\\Desktop\\ai_assistant_tool', 'C:\\Users\\jysatuo\\Desktop\\ai_assistant_tool\\ui', 'C:\\Users\\jysatuo\\Desktop\\ai_assistant_tool\\main', 'C:\\Users\\jysatuo\\Desktop\\ai_assistant_tool\\file', 'C:\\Users\\jysatuo\\Desktop\\ai_assistant_tool\\ai', 'C:\\Users\\jysatuo\\Desktop\\ai_assistant_tool\\ai\\key.json', 'C:\\Users\\jysatuo\\Desktop\\ai_assistant_tool\\main\\ai.ico', 'C:\\Users\\jysatuo\\Desktop\\ai_assistant_tool\\ai'],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\jysatuo\\Desktop\\ai_assistant_tool\\main\\ai.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
