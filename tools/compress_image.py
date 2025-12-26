# tools/compress_image.py
import os
from PIL import Image
import shutil

# 配置
# 获取当前脚本所在的绝对路径 (tools 目录)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 基于脚本位置计算 output 和 assets 的绝对路径
SOURCE_DIR = os.path.join(SCRIPT_DIR, "../output")    # Blender 输出的高清图目录
TARGET_DIR = os.path.join(SCRIPT_DIR, "../assets")    # README 用的图床目录
MAX_WIDTH = 900 # Limit maximal width 
QUALITY = 80                # JPEG 质量 / PNG 压缩等级

def compress_and_move(filename):
    src_path = os.path.join(SOURCE_DIR, filename)
    
    # 自动把文件名里的空格改成下划线 (GitHub 友好)
    clean_name = filename.replace(" ", "_")
    # 给文件名加个后缀表示压缩
    name, ext = os.path.splitext(clean_name)
    clean_name_with_suffix = f"{name}_compressed{ext}"
    dst_path = os.path.join(TARGET_DIR, clean_name_with_suffix)
    
    if not os.path.exists(src_path):
        print(f"❌ 找不到文件: {src_path}")
        return

    try:
        with Image.open(src_path) as img:
            # 1. 如果是透明背景 (RGBA)，保持 PNG，否则转 JPG 更小
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                # 保持 PNG，但优化大小
                # 计算缩放
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                
                img.save(dst_path, "PNG", optimize=True)
                print(f"✅ [PNG] 已压缩并移动: {clean_name}")
                
            else:
                # 转 JPG (体积能小非常多)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                
                # 如果原图是 png，这里强制改为 jpg 后缀
                if dst_path.endswith(".png"):
                    dst_path = dst_path.replace(".png", ".jpg")
                    
                img.save(dst_path, "JPEG", quality=QUALITY, optimize=True)
                print(f"✅ [JPG] 已压缩并移动: {os.path.basename(dst_path)}")

    except Exception as e:
        print(f"❌ 处理出错: {e}")

if __name__ == "__main__":
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        
    print(f"--- 正在处理 Output -> Assets ---")
    
    # 在这里列出你想从 outiput 移动到 assets 的图片名
    # 你只需要改这里的列表
    files_to_process = [
        "1D_Range2.png",
        "1D_Range3.png",
        "2D_Reciprocal.png",
        "3D_Reciprocal.png",
    ]
    
    for f in files_to_process:
        compress_and_move(f)