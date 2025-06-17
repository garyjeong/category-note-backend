from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional
from datetime import datetime


class URLCreate(BaseModel):
    """URL 생성 요청 스키마"""

    url: str
    title: Optional[str] = None
    description: Optional[str] = None

    @field_validator("url")
    @classmethod
    def validate_https_url(cls, v: str) -> str:
        """HTTPS URL만 허용하는 검증"""
        if not v.startswith("https://"):
            raise ValueError("HTTPS URL만 허용됩니다")

        # URL 형식 검증
        try:
            # HttpUrl을 사용하여 URL 형식 검증
            HttpUrl(v)
        except Exception:
            raise ValueError("유효하지 않은 URL 형식입니다")

        return v


class URLResponse(BaseModel):
    """URL 응답 스키마"""

    id: int
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
