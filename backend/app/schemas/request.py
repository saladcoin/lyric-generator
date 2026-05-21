from pydantic import BaseModel
from typing import Optional


class GenerateRequest(BaseModel):
    style: str = "pop"
    emotion: str = "欢快"
    theme: Optional[str] = None
    extra: Optional[str] = None


class GenerateResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
