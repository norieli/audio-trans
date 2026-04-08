"""
手动下载模型脚本
用于解决网络问题，可以预先下载模型

使用方法:
    python download_model.py              # 下载所有模型
    python download_model.py whisper     # 仅下载Whisper模型
    python download_model.py translate   # 仅下载翻译模型
"""
import os
import sys

# 设置镜像站
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# 默认模型
DEFAULT_MODEL = "base"
# 翻译模型
TRANSLATE_MODEL = "Helsinki-NLP/opus-mt-en-zh"
# 模型保存目录
MODEL_DIR = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")


def download_whisper(model_size: str = DEFAULT_MODEL):
    """下载 Whisper 模型"""
    print(f"\n{'='*50}")
    print(f"下载 Whisper {model_size} 模型...")
    print(f"镜像站: https://hf-mirror.com")
    print(f"保存位置: {MODEL_DIR}")
    print('='*50)

    try:
        from faster_whisper import WhisperModel

        # 这会下载模型到缓存目录
        model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

        print(f"[OK] Whisper 模型下载成功!")
        return True

    except Exception as e:
        print(f"[FAIL] 下载失败: {e}")
        return False


def download_translate_model():
    """下载翻译模型"""
    print(f"\n{'='*50}")
    print(f"下载翻译模型: {TRANSLATE_MODEL}")
    print(f"镜像站: https://hf-mirror.com")
    print(f"保存位置: {MODEL_DIR}")
    print('='*50)

    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

        print("下载tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(TRANSLATE_MODEL)

        print("下载模型...")
        model = AutoModelForSeq2SeqLM.from_pretrained(TRANSLATE_MODEL)

        print(f"[OK] 翻译模型下载成功!")
        return True

    except Exception as e:
        print(f"[FAIL] 下载失败: {e}")
        return False


def download_all():
    """下载所有模型"""
    print("\n" + "="*50)
    print("开始下载所有模型...")
    print("="*50)

    success = True

    # 下载Whisper
    if not download_whisper():
        success = False

    # 下载翻译模型
    if not download_translate_model():
        success = False

    return success


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode == "whisper":
        download_whisper()
    elif mode == "translate":
        download_translate_model()
    else:
        download_all()

    print("\n" + "="*50)
    print("模型下载完成!")
    print("="*50)