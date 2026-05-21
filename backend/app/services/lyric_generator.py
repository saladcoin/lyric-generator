from typing import Optional, List
from app.services.llm_client import chat_completion

SYSTEM_PROMPT = """你是一位顶尖的歌词创作大师，擅长流行、摇滚、古风、R&B、民谣、说唱等多种曲风。

【创作原则】
1. 歌词必须富有诗意和美感，语言优美流畅，有韵律感
2. 素材内容仅用于提取情感、意象和主题，不得直接引用其中的技术性描述
3. 严禁在歌词中出现：像素、尺寸、数值、百分比、代码、数据、技术参数等任何数字化或技术化词汇
4. 歌词须包含完整结构：歌名 + 主歌 + 副歌 + 桥段
5. 意象要含蓄优美，用比喻和象征来表达情感"""

STYLE_MAP = {
    "pop": "流行",
    "rock": "摇滚",
    "gufeng": "古风",
    "rnb": "R&B",
    "folk": "民谣",
    "hiphop": "说唱",
}


def build_messages(
    content_text: str,
    style: str,
    emotion: str,
    theme: Optional[str] = None,
    extra: Optional[str] = None,
    image_base64s: Optional[List[str]] = None,
) -> list:
    style_cn = STYLE_MAP.get(style, style)

    user_content = []

    # Add all images first
    if image_base64s:
        for b64 in image_base64s:
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
            })

    # Build the text prompt
    text = f"""【素材内容】
{content_text}

【创作要求】
- 曲风：{style_cn}
- 情感基调：{emotion}
"""
    if theme:
        text += f"- 主题：{theme}\n"
    if extra:
        text += f"- 额外要求：{extra}\n"

    text += """
⚠️ 重要提醒：歌词中不得出现任何数字、像素、尺寸、技术参数等词汇，务必用诗意的语言来表达。

请创作一首完整的歌词，包含歌名和段落结构（主歌、副歌、桥段等）。"""

    user_content.append({"type": "text", "text": text})

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]


def generate_lyrics(
    content_text: str,
    style: str,
    emotion: str,
    theme: Optional[str] = None,
    extra: Optional[str] = None,
    image_base64s: Optional[List[str]] = None,
) -> str:
    messages = build_messages(content_text, style, emotion, theme, extra, image_base64s)
    return chat_completion(messages)
