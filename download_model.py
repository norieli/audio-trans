"""
手动下载 Whisper 模型脚本
用于解决网络问题，可以预先下载模型

使用方法:
    python download_model.py

或指定模型大小:
    python download_model.py base
"""
import os
import sys

# 设置镜像站
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# 默认模型
DEFAULT_MODEL = "base"
# 模型保存目录
MODEL_DIR = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")

def download_model(model_size: str = DEFAULT_MODEL):
    """下载 Whisper 模型"""
    print(f"开始下载 Whisper {model_size} 模型...")
    print(f"镜像站: https://hf-mirror.com")
    print(f"保存位置: {MODEL_DIR}")
    print("-" * 50)

    try:
        from faster_whisper import WhisperModel

        # 这会下载模型到缓存目录
        model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

        print("-" * 50)
        print(f"[OK] 模型下载成功!")
        print(f"模型位置: {MODEL_DIR}")
        return True

    except Exception as e:
        print("-" * 50)
        print(f"[FAIL] 下载失败: {e}")
        print("\n尝试其他方法...")

        # 尝试使用 huggingface-cli 下载
        try:
            print("\n使用 huggingface-cli 下载...")
            os.system(f"huggingface-cli download --local-dir {MODEL_DIR} --resume-download counterparty.ctl/{model_size}-whisper")
        except:
            pass

        return False


if __name__ == "__main__":
    model_size = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL
    download_model(model_size)

    print("\n" + "=" * 50)
    print("手动下载方法:")
    print("1. 访问: https://hf-mirror.com/models")
    print("2. 搜索: faster-whisper/{model_size}")
    print("3. 下载 model.onnx 和 config.json")
    print("4. 保存到: %s" % MODEL_DIR)
    print("=" * 50)