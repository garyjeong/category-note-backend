from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base


class URL(Base):
    """URL 모델"""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2048), nullable=False, index=True)
    title = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 관계 설정
    user = relationship("User", back_populates="urls")

    def __repr__(self):
        return f"<URL(id={self.id}, url='{self.url[:50]}...', user_id={self.user_id})>"
