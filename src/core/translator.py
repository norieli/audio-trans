"""
Translator - Local and AI translation
翻译器 - 本地翻译和AI翻译
"""
import os
import re
import requests
from pathlib import Path
from typing import List, Tuple, Optional

# 设置大陆镜像源
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# 本地翻译模型
LOCAL_MODEL = None
LOCAL_TRANSLATOR = None


def load_local_model():
    """Load local translation model (lazy load)"""
    global LOCAL_MODEL, LOCAL_TRANSLATOR
    if LOCAL_TRANSLATOR is None:
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            print("Loading local translation model...")
            # 使用轻量级英中翻译模型
            model_name = "Helsinki-NLP/opus-mt-en-zh"
            LOCAL_MODEL = model_name
            LOCAL_TRANSLATOR = {
                "tokenizer": AutoTokenizer.from_pretrained(model_name),
                "model": AutoModelForSeq2SeqLM.from_pretrained(model_name)
            }
            print("Local translation model loaded!")
        except Exception as e:
            print(f"Failed to load local model: {e}")
            LOCAL_TRANSLATOR = None
    return LOCAL_TRANSLATOR is not None


class Translator:
    """Handles subtitle translation (local or AI)"""

    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

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
        Local translation using CSANMT model (Hugging Face)
        本地翻译使用CSANMT模型
        """
        try:
            # 懒加载模型
            if not load_local_model():
                return "[错误: 本地模型加载失败，请检查transformers库]"

            tokenizer = LOCAL_TRANSLATOR["tokenizer"]
            model = LOCAL_TRANSLATOR["model"]

            # 翻译文本
            inputs = tokenizer(text, return_tensors="pt", padding=True)

            # 生成翻译
            outputs = model.generate(**inputs, max_new_tokens=256)

            translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return translated

        except Exception as e:
            print(f"Local translation error: {e}")
            return f"[翻译失败: {str(e)[:50]}]"

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
        """Check if network is available (mainly for AI translation)"""
        try:
            requests.get("https://api.deepseek.com", timeout=5)
            return True
        except:
            return False