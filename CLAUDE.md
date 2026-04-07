# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AudioTrans AI (音转译 AI) - A Windows desktop application for audio file organization, subtitle transcription (Whisper), and translation (local CSANMT model or DeepSeek AI API).

## Tech Stack

- **Language**: Python 3.8~3.10 (64-bit)
- **UI Framework**: PyQt5
- **Audio Transcription**: faster-whisper (Whisper base model)
- **Translation**: CSANMT (local) + DeepSeek AI API (cloud)
- **File Operations**: os/shutil
- **Packaging**: PyInstaller (single .exe, ~300MB)

## Architecture

Three-layer architecture:

1. **Frontend Layer** (UI): PyQt5-based interface with 12-step wizard workflow
2. **Core Function Layer**: 12 independent modules implementing the workflow
3. **Base Dependency Layer**: Models, APIs, system adapters

## Common Commands

```bash
# Install dependencies
pip install pyqt5 faster-whisper requests

# Run development
python main.py

# Package as .exe
pyinstaller --onefile --name AudioTransAI --add-data "models;models" main.py
```

## 12-Step Core Workflow

1. **Select Directories** - Choose source MP3 directory and output directory
2. **Filename Matching** - Filter files by keyword/prefix/suffix rules
3. **New Filename Rules** - Set prefix + preserve original name OR sequential numbering
4. **Organize Files** - Copy or move matched MP3 files to output
5. **Confirm Structure** - User verifies directory organization
6. **Generate First Subtitle** - Test Whisper transcription on first file → .lrc format
7. **Review First Subtitle** - User validates transcription quality
8. **Batch Subtitles** - Generate .lrc for all files (supports pause/continue/terminate)
9. **Translate First Subtitle** - Local CSANMT or DeepSeek AI (en→zh)
10. **Review Translation** - User validates translation quality
11. **Batch Translation** - Generate translation .txt files for all subtitles
12. **Complete** - Show summary, open output, restart option

## Key Implementation Details

- **API Key Storage**: DeepSeek API key stored as base64-encoded string in local temp config
- **Model Loading**: Whisper model loads once at startup, reused for all transcriptions
- **Batch Processing**: Supports pause/continue/terminate, resumes after interrupt
- **Exception Handling**: All core operations wrapped in try-except; user-friendly error messages
- **Output Format**: Subtitles as .lrc (with timestamps), translations as .txt (bilingual format)

## Output File Naming

- Audio: `{new_filename}.mp3`
- Subtitle: `{new_filename}.lrc`
- Translation: `{new_filename}_中文翻译.txt`

## Constraints

- Windows 10/11 (64-bit) only
- Target: i5 + 8GB RAM laptop
- Performance: ≤90s per 3-min audio transcription, ≤30s per translation
- No external models required - all bundled with PyInstaller