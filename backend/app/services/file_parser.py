from pathlib import Path
from typing import Union
from io import BytesIO
import base64

from PIL import Image


def parse_txt(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def parse_pdf(file_path: Path) -> str:
    try:
        import fitz
        text_parts = []
        doc = fitz.open(str(file_path))
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        return "\n".join(text_parts)
    except ImportError:
        return "[PDF 解析库不可用，请安装 PyMuPDF]"


def parse_docx(file_path: Path) -> str:
    try:
        from docx import Document
        doc = Document(str(file_path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except ImportError:
        return "[DOCX 解析库不可用，请安装 python-docx]"


def image_to_base64(file_path: Path) -> str:
    with Image.open(file_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        buf = BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")


def describe_image(file_path: Path) -> str:
    """Describe image in poetic language for the LLM, avoiding raw technical terms."""
    with Image.open(file_path) as img:
        w, h = img.size
        small = img.resize((100, 100)).convert("RGB")
        pixels = list(small.getdata())
        r_avg = sum(p[0] for p in pixels) // len(pixels)
        g_avg = sum(p[1] for p in pixels) // len(pixels)
        b_avg = sum(p[2] for p in pixels) // len(pixels)

    brightness = (r_avg + g_avg + b_avg) / 3

    # Brightness → atmosphere
    if brightness > 200:
        atmosphere = "明亮温暖，充满了光线，像是阳光明媚的白昼"
    elif brightness > 150:
        atmosphere = "光线柔和适中，氛围宁静平和"
    elif brightness > 100:
        atmosphere = "光线偏暗，带着几分沉静与忧郁，像黄昏或阴天的氛围"
    else:
        atmosphere = "昏暗深沉，像是夜晚或幽暗的空间，充满神秘感"

    # Color → mood
    def color_mood(r, g, b):
        if r > 200 and g > 200 and b > 200:
            return "整体色调偏浅淡"
        if r < 60 and g < 60 and b < 60:
            return "整体色调深暗"
        if r > max(g, b):
            return "带有暖色调，给人热烈或温暖的感觉"
        if g > max(r, b):
            return "带有清新自然的色调"
        if b > max(r, g):
            return "带有冷色调，显得宁静而深邃"
        return "色彩丰富多变"

    # Composition → feeling
    ratio = w / h
    if ratio > 1.4:
        composition = "视野开阔，横向延展，像一幅壮阔的风景画卷"
    elif ratio < 0.7:
        composition = "构图修长，聚焦于主体，有一种凝练的美感"
    else:
        composition = "构图均衡稳定，给人以平和协调之感"

    lines = [
        "以下是对这幅画面的意境描述（请据此创作歌词，不要提及任何技术参数）：",
        f"这幅画面{composition}。",
        f"光线{atmosphere}。",
        f"{color_mood(r_avg, g_avg, b_avg)}。",
    ]
    return "\n".join(lines)


def parse_file(file_path: Path) -> Union[str, dict]:
    suffix = file_path.suffix.lower()

    if suffix == ".txt":
        return {"type": "text", "content": parse_txt(file_path)}
    elif suffix == ".pdf":
        return {"type": "text", "content": parse_pdf(file_path)}
    elif suffix == ".docx":
        return {"type": "text", "content": parse_docx(file_path)}
    elif suffix in (".png", ".jpg", ".jpeg"):
        b64 = image_to_base64(file_path)
        desc = describe_image(file_path)
        return {"type": "image", "base64": b64, "text_desc": desc}
    else:
        raise ValueError(f"不支持的文件类型: {suffix}")
