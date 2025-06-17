from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field, validator


class BookmarkNoteCreate(BaseModel):
    """북마크 노트 생성 스키마"""

    url: HttpUrl = Field(..., description="북마크할 URL (HTTPS만 허용)")

    @validator("url")
    def validate_https_url(cls, v):
        if not str(v).startswith("https://"):
            raise ValueError("HTTPS URL만 허용됩니다")
        return v


class BookmarkNoteResponse(BaseModel):
    """북마크 노트 응답 스키마"""

    id: int
    title: str
    url: str
    category1: Optional[str] = None
    category2: Optional[str] = None
    category3: Optional[str] = None
    description: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BookmarkNoteCategoryUpdate(BaseModel):
    """북마크 노트 카테고리 업데이트 스키마"""

    category1: Optional[str] = Field(
        None, max_length=100, description="첫 번째 카테고리"
    )
    category2: Optional[str] = Field(
        None, max_length=100, description="두 번째 카테고리"
    )
    category3: Optional[str] = Field(
        None, max_length=100, description="세 번째 카테고리"
    )


class BookmarkNoteListResponse(BaseModel):
    """북마크 노트 리스트 응답 스키마"""

    items: List[BookmarkNoteResponse]
    total: int
    page: int
    size: int
    pages: int


class BookmarkNoteFilter(BaseModel):
    """북마크 노트 필터링 스키마"""

    category: Optional[str] = Field(None, description="카테고리로 필터링")
    search: Optional[str] = Field(None, description="제목 또는 설명에서 검색")
    page: int = Field(1, ge=1, description="페이지 번호")
    size: int = Field(20, ge=1, le=100, description="페이지 크기")
