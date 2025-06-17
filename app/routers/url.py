from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.routers.auth import get_current_user
from app.controllers.bookmark_controller import BookmarkController
from app.schemas.bookmark import BookmarkNoteCreate, BookmarkNoteResponse
from app.models.user import User

router = APIRouter()


@router.post("/url", response_model=BookmarkNoteResponse, status_code=201)
async def create_url(
    url_data: BookmarkNoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    URL 등록 및 북마크 노트 생성

    - **url**: HTTPS로 시작하는 유효한 URL (필수)
    - 나중에 AI를 통해 제목과 카테고리가 자동 생성됩니다

    JWT 토큰 인증이 필요합니다.
    """
    try:
        # 북마크 노트 생성
        bookmark_note = BookmarkController.create_bookmark_note(
            db=db, bookmark_data=url_data, user_id=current_user.id
        )

        return bookmark_note
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"북마크 노트 생성 중 오류가 발생했습니다: {str(e)}",
        )
