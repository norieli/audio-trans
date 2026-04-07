"""
Translator - Local and AI translation
翻译器 - 本地翻译和AI翻译
"""
import os
import re
import requests
from pathlib import Path
from typing import List, Tuple, Optional


class Translator:
    """Handles subtitle translation (local or AI)"""

    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    # Free translation API (MyMemory)
    MYMEMORY_API_URL = "https://api.mymemory.translated.net/get"

    def __init__(self, mode: str = "local"):
        """
        Initialize translator
        mode: local or ai
        """
        self.mode = mode
        self.api_key = ""

    def set_api_key(self, api_key: str):
        """Set DeepSeek API key"""
        self.api_key = api_key

    def translate_lrc(self, lrc_path: str, output_path: str = None) -> Tuple[bool, str]:
        """
        Translate LRC file content
        Returns: (success, output_path_or_error)
        """
        try:
            # Read LRC file
            with open(lrc_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Get audio filename for output naming
            audio_name = Path(lrc_path).stem
            if output_path is None:
                output_path = os.path.join(
                    os.path.dirname(lrc_path),
                    f"{audio_name}.txt"  # 和音频名称一致
                )

            # Translate each line
            translations = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Extract text after timestamp [mm:ss.xx]
                match = re.match(r'\[\d{2}:\d{2}\.\d{2}\]\s*(.+)', line)
                if match:
                    text = match.group(1).strip()
                    if text:
                        # Translate this line
                        if self.mode == "ai" and self.api_key:
                            translated = self._translate_ai(text)
                        else:
                            translated = self._translate_local(text)

                        translations.append(f"{text}\n{translated}")

            # Write translation file (bilingual format)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n\n".join(translations))

            return True, output_path

        except Exception as e:
            return False, str(e)

    def batch_translate(self, lrc_files: List[str], output_dir: str,
                       progress_callback=None) -> Tuple[int, int]:
        """
        Batch translate LRC files
        Returns: (success_count, fail_count)
        """
        success = 0
        failed = 0

        total = len(lrc_files)
        for i, lrc_file in enumerate(lrc_files):
            if progress_callback:
                progress_callback(i, total, Path(lrc_file).name)

            audio_name = Path(lrc_file).stem
            txt_path = os.path.join(output_dir, f"{audio_name}.txt")  # 和音频名称一致

            # Skip if already exists
            if os.path.exists(txt_path):
                success += 1
                continue

            ok, result = self.translate_lrc(lrc_file, txt_path)
            if ok:
                success += 1
            else:
                failed += 1
                print(f"Failed to translate {lrc_file}: {result}")

        return success, failed

    def _translate_local(self, text: str) -> str:
        """
        Local translation using free MyMemory API
        """
        try:
            params = {
                "q": text,
                "langpair": "en|zh"
            }
            response = requests.get(
                self.MYMEMORY_API_URL,
                params=params,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("responseStatus") == 200:
                    return data.get("responseData", {}).get("translatedText", text)
            return text
        except Exception as e:
            # Fallback: return original text
            print(f"Local translation error: {e}")
            return text

    def _translate_ai(self, text: str) -> str:
        """
        Translate using DeepSeek AI API
        """
        if not self.api_key:
            return "[错误: 未配置API Key]"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional translator. Translate the following English text to Chinese. Only return the translated text, nothing else."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            "max_tokens": 1024,
            "temperature": 0.3
        }

        try:
            response = requests.post(
                self.DEEPSEEK_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"[翻译失败: {response.status_code}]"
        except requests.RequestException as e:
            return f"[翻译失败: 网络错误]"

    def check_network(self) -> bool:
        """Check if network is available"""
        try:
            requests.get("https://api.mymemory.translated.net", timeout=5)
            return True
        except:
            return False