"""
AudioTrans AI - Main Entry Point
音转译 AI - 主程序入口
"""
import sys
import os
import traceback

# IMPORTANT: Set HuggingFace mirror BEFORE importing faster-whisper
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_MIRROR"] = "https://hf-mirror.com"

# Pre-load the model to avoid Qt threading issues
print("[Main] Pre-loading Whisper model...")
sys.stdout.flush()

WHISPER_MODEL = None
try:
    from src.core.whisper_transcriber import WhisperTranscriber
    WHISPER_MODEL = WhisperTranscriber("base")
    print("[Main] Whisper model pre-loaded successfully!")
    sys.stdout.flush()
except Exception as e:
    print(f"[Main] Warning: Could not pre-load model: {e}")
    sys.stdout.flush()

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def exception_hook(exctype, value, tb):
    """Global exception handler"""
    import traceback
    traceback.print_exception(exctype, value, tb)
    sys.__excepthook__(exctype, value, tb)


def main():
    """Application entry point"""
    # Install exception hook
    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    app.setApplicationName("AudioTrans AI")
    app.setOrganizationName("AudioTrans")

    print("[Main] Starting AudioTrans AI...")
    sys.stdout.flush()

    try:
        window = MainWindow(whisper_model=WHISPER_MODEL)
        window.show()
        print("[Main] Window shown successfully")
        sys.stdout.flush()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"[Main] FATAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()