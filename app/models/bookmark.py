from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base


class BookmarkNote(Base):
    """북마크 노트 모델"""

    __tablename__ = "bookmark_notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)  # 요약된 제목
    url = Column(
        String(2048), nullable=False
    )  # 원본 URL (인덱스 제거 - 너무 긴 필드)
    category1 = Column(
        String(100), nullable=True, index=True
    )  # 첫 번째 카테고리
    category2 = Column(
        String(100), nullable=True, index=True
    )  # 두 번째 카테고리
    category3 = Column(
        String(100), nullable=True, index=True
    )  # 세 번째 카테고리
    description = Column(Text, nullable=True)  # 추가 설명
    is_deleted = Column(
        Boolean, default=False, nullable=False, index=True
    )  # 소프트 삭제
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # 삭제 일자

    # 관계 설정
    user = relationship("User", back_populates="bookmark_notes")

    def __repr__(self):
        return f"<BookmarkNote(id={self.id}, title='{self.title[:30]}...', user_id={self.user_id})>"
