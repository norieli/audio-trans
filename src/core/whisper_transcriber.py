"""
Whisper Transcription - Audio to subtitle conversion
Whisper转写 - 音频转字幕
"""
import os
import sys
import time
from pathlib import Path
from typing import List, Tuple, Optional

# 设置HuggingFace镜像站 (大陆优化) - 必须在 import 之前设置!
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_MIRROR"] = "https://hf-mirror.com"

from faster_whisper import WhisperModel

import traceback


class WhisperTranscriber:
    """Handles audio transcription using Whisper"""

    def __init__(self, model_size: str = "base", model_path: str = None):
        """
        Initialize Whisper model
        Args:
            model_size: base, small, medium, large
            model_path: Optional local path to model (for offline use)
        """
        self.model = None
        self.model_size = model_size
        self.model_path = model_path
        print(f"[WhisperTranscriber] Initializing with model_size={model_size}")
        sys.stdout.flush()
        self._load_model()
        print(f"[WhisperTranscriber] Initialization complete")

    def _load_model(self):
        """Load Whisper model"""
        print(f"[_load_model] Loading Whisper {self.model_size} model...")
        sys.stdout.flush()

        # Use float32 for maximum compatibility
        try:
            print(f"[_load_model] Creating WhisperModel with float32...")
            sys.stdout.flush()

            self.model = WhisperModel(
                self.model_size,
                device="cpu",
                compute_type="float32"
            )
            print(f"[_load_model] Model created successfully!")
            sys.stdout.flush()
            return
        except Exception as e:
            error_msg = str(e)
            print(f"[_load_model] ERROR: {error_msg}")
            traceback.print_exc()
            sys.stdout.flush()
            raise
        for attempt in range(max_retries):
            try:
                self.model = WhisperModel(
                    self.model_size,
                    device="cpu",
                    compute_type="int8"
                )
                print("Model loaded successfully")
                return
            except Exception as e:
                error_msg = str(e)
                print(f"Attempt {attempt + 1}/{max_retries} failed: {error_msg}")

                # Check for common network errors
                if any(x in error_msg.lower() for x in ["connection", "network", "timeout", "huggingface", "hub"]):
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 5  # 5, 10, 15 seconds
                        print(f"Network error detected, retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        raise Exception(
                            "模型下载失败，可能是网络问题。\n"
                            "解决方案：\n"
                            "1. 检查网络连接\n"
                            "2. 手动下载模型后配置本地路径\n"
                            "3. 或使用科学上网\n"
                            f"错误详情: {error_msg}"
                        )
                else:
                    raise

    def transcribe(self, audio_path: str, language: str = None) -> Tuple[bool, str, str]:
        """
        Transcribe audio file to text
        Returns: (success, text, error_message)
        """
        if not self.model:
            return False, "", "模型未加载，请重启程序"

        try:
            segments, info = self.model.transcribe(
                audio_path,
                language=language,  # None for auto-detect
                beam_size=5,
                vad_filter=True
            )

            # Collect all segments
            lrc_lines = []

            for segment in segments:
                text = segment.text.strip()
                if text:
                    # LRC format: [mm:ss.xx] text
                    start_time = self._format_lrc_time(segment.start)
                    lrc_lines.append(f"[{start_time}] {text}")

            return True, "\n".join(lrc_lines), ""
        except Exception as e:
            return False, "", str(e)

    def transcribe_to_lrc(self, audio_path: str, output_path: str = None) -> Tuple[bool, str]:
        """
        Transcribe audio and save as LRC file
        Returns: (success, output_path_or_error)
        """
        success, lrc_content, error = self.transcribe(audio_path)

        if not success:
            return False, error

        if output_path is None:
            audio_name = Path(audio_path).stem
            output_path = f"{audio_name}.lrc"

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(lrc_content)
            return True, output_path
        except Exception as e:
            return False, str(e)

    def batch_transcribe(self, audio_files: List[str], output_dir: str,
                        progress_callback=None) -> Tuple[int, int]:
        """
        Batch transcribe audio files
        Returns: (success_count, fail_count)
        """
        if not self.model:
            return 0, len(audio_files)

        success = 0
        failed = 0

        total = len(audio_files)
        for i, audio_file in enumerate(audio_files):
            if progress_callback:
                progress_callback(i, total, Path(audio_file).name)

            audio_name = Path(audio_file).stem
            lrc_path = os.path.join(output_dir, f"{audio_name}.lrc")

            # Skip if already exists
            if os.path.exists(lrc_path):
                success += 1
                continue

            ok, result = self.transcribe_to_lrc(audio_file, lrc_path)
            if ok:
                success += 1
            else:
                failed += 1
                print(f"Failed to transcribe {audio_file}: {result}")

        return success, failed

    @staticmethod
    def _format_lrc_time(seconds: float) -> str:
        """Format seconds to LRC timestamp [mm:ss.xx]"""
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes:02d}:{secs:05.2f}"