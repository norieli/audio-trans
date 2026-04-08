# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller build script for AudioTrans AI
构建脚本 - 使用 PyInstaller 打包为 exe
"""

import PyInstaller.__main__
import os

# 添加icons目录到数据文件
icon_path = ''
if os.path.exists('icons'):
    icon_path = '--add-data=icons;icons'

PyInstaller.__main__.run([
    'main.py',
    '--name=AudioTransAI',
    '--onefile',
    '--windowed',
    '--icon=icons/icon.ico',
    '--add-data=src;src',
    icon_path,
    '--hidden-import=PyQt5',
    '--hidden-import=PyQt5.QtCore',
    '--hidden-import=PyQt5.QtGui',
    '--hidden-import=PyQt5.QtWidgets',
    '--hidden-import=faster_whisper',
    '--hidden-import=requests',
    '--hidden-import=transformers',
    '--hidden-import=tokenizers',
    '--hidden-import=sentencepiece',
    '--hidden-import=torch',
    '--hidden-import=torch.nn',
    '--hidden-import=sacremoses',
    '--collect-all=faster_whisper',
    '--collect-all=transformers',
    '--collect-all=tokenizers',
    '--collect-all=sentencepiece',
    '--noconfirm',
    '--clean',
])