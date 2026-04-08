# AudioTrans AI 音转译 AI

Windows桌面应用程序 - 音频整理、字幕转写、翻译一体化工具

## 功能特点

- **音频整理** - 按关键词/前缀/后缀递归筛选MP3文件，支持重命名
- **字幕转写** - 基于Whisper AI的音频转字幕(LRC格式)，支持批量处理
- **双语翻译** - 本地CSANMT模型(离线)或DeepSeek AI翻译
- **12步向导** - 简洁易用的向导流程

## 系统要求

- Windows 10/11 (64位)
- Python 3.8~3.10
- 内存 8GB+

## 安装

```bash
# 克隆项目
git clone <repository-url>
cd audio-trans

# 安装依赖
pip install -r requirements.txt

# 预下载模型 (可选，解决首次加载慢的问题)
python download_model.py
```

## 使用方法

```bash
# 运行程序
python main.py
```

### 12步流程

1. 选择源音频目录和输出目录
2. 设置文件名匹配规则 (关键词/前缀/后缀)
3. 设置新文件名规则 (保留原名/前缀+序号/仅序号)
4. 复制或移动文件到输出目录
5. 确认目录结构
6. 生成第一个字幕 (测试转写效果)
7. 查看字幕内容
8. 批量生成所有字幕
9. 翻译第一个字幕 (本地API/DeepSeek AI)
10. 查看翻译效果
11. 批量翻译
12. 完成

## 打包

```bash
# 打包为单个exe
pyinstaller --onefile --name AudioTransAI main.py
```

## 依赖

- PyQt5 >= 5.15.0
- faster-whisper >= 0.10.0
- requests >= 2.28.0
- transformers >= 4.30.0
- torch >= 2.0.0
- sentencepiece >= 0.1.99

## 配置

- API Key存储: `~/.audiotrans/config.json` (base64编码)
- 模型: Whisper base + Helsinki-NLP翻译模型 (首次运行自动下载)

## 输出文件

- 音频: `{新文件名}.mp3`
- 字幕: `{新文件名}.lrc`
- 翻译: `{新文件名}.txt` (与音频名一致)

## 许可证

MIT License

## 作者

Norie