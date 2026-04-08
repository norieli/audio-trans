"""
生成应用图标
使用PIL生成一个简单的AudioTrans AI图标
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 创建一个简单的图标
def create_icon():
    # 创建256x256的图标
    size = 256
    img = Image.new('RGB', (size, size), color='#2563eb')  # 蓝色背景

    draw = ImageDraw.Draw(img)

    # 画一个圆形的音频波形图案
    center = size // 2

    # 画外圈
    draw.ellipse([20, 20, 236, 236], outline='white', width=8)

    # 画音频波形（三条竖线）
    bar_width = 20
    bar_spacing = 30
    start_x = center - bar_spacing

    # 左侧条
    draw.rectangle([start_x - bar_width, 80, start_x, 176], fill='white')
    # 中间条
    draw.rectangle([start_x, 60, start_x + bar_width, 196], fill='white')
    # 右侧条
    draw.rectangle([start_x + bar_width, 90, start_x + 2 * bar_width, 166], fill='white')

    # 绘制 "AT" 文字
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()

    # 在图标底部添加小字
    draw.text((center - 40, 200), "AT", fill='white', font=font)

    return img


def create_icon_file():
    """生成图标文件"""
    # 确保icons目录存在
    icons_dir = os.path.join(os.path.dirname(__file__), 'icons')
    os.makedirs(icons_dir, exist_ok=True)

    # 创建图标
    img = create_icon()

    # 保存为PNG
    png_path = os.path.join(icons_dir, 'icon.png')
    img.save(png_path)
    print(f"Created: {png_path}")

    # 创建ICO文件（多尺寸）
    ico_path = os.path.join(icons_dir, 'icon.ico')

    # 生成多个尺寸的图标
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icons = []
    for s in sizes:
        icons.append(img.resize(s, Image.LANCZOS))

    # 保存为ICO
    icons[0].save(ico_path, format='ICO', sizes=[(s[0], s[1]) for s in sizes], append_images=icons[1:])
    print(f"Created: {ico_path}")

    return ico_path


if __name__ == "__main__":
    path = create_icon_file()
    print(f"\nIcon created at: {path}")