from sqlalchemy.orm import Session
from app.models.url import URL
from app.models.user import User
from app.schemas.url import URLCreate


class URLController:
    """URL 관련 비즈니스 로직 컨트롤러"""

    @staticmethod
    def create_url(db: Session, url_data: URLCreate, user: User) -> URL:
        """새 URL 생성"""
        db_url = URL(
            url=url_data.url,
            title=url_data.title,
            description=url_data.description,
            user_id=user.id,
        )
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        return db_url
