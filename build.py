# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller build script for AudioTrans AI
构建脚本 - 使用 PyInstaller 打包为 exe
"""

import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--name=AudioTransAI',
    '--onefile',
    '--windowed',
    '--icon=NONE',
    '--add-data=src;src',
    '--hidden-import=PyQt5',
    '--hidden-import=PyQt5.QtCore',
    '--hidden-import=PyQt5.QtGui',
    '--hidden-import=PyQt5.QtWidgets',
    '--hidden-import=faster_whisper',
    '--hidden-import=requests',
    '--collect-all=faster_whisper',
    '--noconfirm',
    '--clean',
])