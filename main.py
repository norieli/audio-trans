"""
AudioTrans AI - Main Entry Point
音转译 AI - 主程序入口
"""
import sys
import os
import traceback

# Helper function to safely print and flush
def log(msg):
    """Safe print and flush for both console and windowed mode"""
    print(msg)
    if sys.stdout:
        sys.stdout.flush()

# IMPORTANT: Set HuggingFace mirror BEFORE importing faster-whisper
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_MIRROR"] = "https://hf-mirror.com"

# Pre-load the model to avoid Qt threading issues
log("[Main] Pre-loading Whisper model...")

WHISPER_MODEL = None
try:
    from src.core.whisper_transcriber import WhisperTranscriber
    WHISPER_MODEL = WhisperTranscriber("base")
    log("[Main] Whisper model pre-loaded successfully!")
except Exception as e:
    log(f"[Main] Warning: Could not pre-load model: {e}")

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
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

    # Set app icon
    icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Apply dark theme
    from ui.theme import MAIN_STYLE
    app.setStyleSheet(MAIN_STYLE)

    log("[Main] Starting AudioTrans AI...")

    try:
        window = MainWindow(whisper_model=WHISPER_MODEL)
        window.show()
        log("[Main] Window shown successfully")
        sys.exit(app.exec_())
    except Exception as e:
        log(f"[Main] FATAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()