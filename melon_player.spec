# -*- mode: python ; coding: utf-8 -*-
import os

# VLC DLL/플러그인은 번들하지 않음 → 설치된 VLC를 런타임에 직접 사용
vlc_binaries = []
vlc_datas    = []

a = Analysis(
    ["melon_player.py"],
    pathex=[],
    binaries=vlc_binaries,
    datas=vlc_datas,
    hiddenimports=[
        "vlc",
        "bs4",
        "bs4.builder._htmlparser",
        "yt_dlp",
        "yt_dlp.extractor",
        "yt_dlp.extractor.youtube",
        "yt_dlp.postprocessor",
        "requests",
        "certifi",
        "charset_normalizer",
        "urllib3",
        "tkinter",
        "tkinter.ttk",
        "tkinter.messagebox",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["matplotlib", "numpy", "PIL", "scipy", "pandas"],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="차트100플레이어",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,        # GUI 앱 → 콘솔 창 숨김
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
