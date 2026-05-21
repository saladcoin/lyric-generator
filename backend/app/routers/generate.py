import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from app.services.file_parser import parse_file
from app.services.lyric_generator import generate_lyrics
from app.schemas.request import GenerateResponse

router = APIRouter(prefix="/api", tags=["generate"])


@router.post("/generate", response_model=GenerateResponse)
async def generate(
    files: List[UploadFile] = File(None),
    style: str = Form("pop"),
    emotion: str = Form("欢快"),
    theme: str = Form(None),
    extra: str = Form(None),
):
    try:
        text_parts = []
        image_base64s = []

        if files:
            for file in files:
                if not file.filename:
                    continue
                suffix = Path(file.filename).suffix.lower()
                if suffix not in ALLOWED_EXTENSIONS:
                    raise HTTPException(
                        400, f"不支持的文件类型: {suffix}，支持 {ALLOWED_EXTENSIONS}"
                    )

                file_id = uuid.uuid4().hex
                save_path = UPLOAD_DIR / f"{file_id}{suffix}"
                data = await file.read()

                if len(data) > MAX_FILE_SIZE:
                    raise HTTPException(400, "文件大小超过 10MB 限制")

                with open(save_path, "wb") as f:
                    f.write(data)

                parsed = parse_file(save_path)
                if parsed["type"] == "image":
                    text_parts.append(parsed["text_desc"])
                    image_base64s.append(parsed["base64"])
                else:
                    text_parts.append(parsed["content"])
                save_path.unlink(missing_ok=True)

        content_text = "\n\n".join(text_parts) if text_parts else ""
        if not content_text and not image_base64s:
            content_text = "（用户没有提供素材，请根据曲风和情感直接创作一首原创歌词）"

        lyrics = generate_lyrics(
            content_text=content_text,
            style=style,
            emotion=emotion,
            theme=theme,
            extra=extra,
            image_base64s=image_base64s if image_base64s else None,
        )

        return GenerateResponse(
            success=True,
            data={
                "lyrics": lyrics,
                "style": style,
                "emotion": emotion,
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        return GenerateResponse(success=False, error=str(e))
