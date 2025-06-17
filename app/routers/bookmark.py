from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.routers.auth import get_current_user
from app.controllers.bookmark_controller import BookmarkController
from app.schemas.bookmark import (
    BookmarkNoteCreate,
    BookmarkNoteResponse,
    BookmarkNoteListResponse,
    BookmarkNoteCategoryUpdate,
)
from app.models.user import User
import math

router = APIRouter(prefix="/api/bookmark", tags=["bookmark"])


@router.post("/", response_model=BookmarkNoteResponse)
async def create_bookmark_note(
    bookmark_data: BookmarkNoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    북마크 노트 생성

    - **url**: 북마크할 URL (HTTPS만 허용)
    - 나중에 AI를 통해 제목과 카테고리가 자동 생성됩니다
    """
    bookmark_note = BookmarkController.create_bookmark_note(
        db=db, bookmark_data=bookmark_data, user_id=current_user.id
    )
    return bookmark_note


@router.get("/", response_model=BookmarkNoteListResponse)
async def get_bookmark_notes(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    category: Optional[str] = Query(None, description="카테고리로 필터링"),
    search: Optional[str] = Query(None, description="제목 또는 설명에서 검색"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    북마크 노트 리스트 조회 (페이지네이션)

    - **page**: 페이지 번호 (1부터 시작)
    - **size**: 페이지 크기 (1-100)
    - **category**: 카테고리로 필터링 (선택사항)
    - **search**: 제목 또는 설명에서 검색 (선택사항)
    """
    bookmark_notes, total = BookmarkController.get_bookmark_notes(
        db=db,
        user_id=current_user.id,
        page=page,
        size=size,
        category=category,
        search=search,
    )

    pages = math.ceil(total / size) if total > 0 else 0

    return BookmarkNoteListResponse(
        items=bookmark_notes, total=total, page=page, size=size, pages=pages
    )


@router.get("/{bookmark_id}", response_model=BookmarkNoteResponse)
async def get_bookmark_note(
    bookmark_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    특정 북마크 노트 조회

    - **bookmark_id**: 조회할 북마크 노트 ID
    """
    bookmark_note = BookmarkController.get_bookmark_note(
        db=db, bookmark_id=bookmark_id, user_id=current_user.id
    )
    return bookmark_note


@router.put("/{bookmark_id}/categories", response_model=BookmarkNoteResponse)
async def update_bookmark_categories(
    bookmark_id: int,
    category_data: BookmarkNoteCategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    북마크 노트 카테고리 업데이트

    - **bookmark_id**: 업데이트할 북마크 노트 ID
    - **category1**: 첫 번째 카테고리
    - **category2**: 두 번째 카테고리
    - **category3**: 세 번째 카테고리
    """
    bookmark_note = BookmarkController.update_bookmark_categories(
        db=db,
        bookmark_id=bookmark_id,
        user_id=current_user.id,
        category_data=category_data,
    )
    return bookmark_note


@router.delete("/{bookmark_id}", response_model=BookmarkNoteResponse)
async def delete_bookmark_note(
    bookmark_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    북마크 노트 삭제 (소프트 삭제)

    - **bookmark_id**: 삭제할 북마크 노트 ID
    - 실제로는 삭제되지 않고 is_deleted 플래그가 True로 설정됩니다
    """
    bookmark_note = BookmarkController.delete_bookmark_note(
        db=db, bookmark_id=bookmark_id, user_id=current_user.id
    )
    return bookmark_note


@router.get("/categories/list", response_model=List[str])
async def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    사용자의 모든 카테고리 조회

    - 현재 사용자가 생성한 모든 북마크 노트의 카테고리 목록을 반환합니다
    """
    categories = BookmarkController.get_categories(
        db=db, user_id=current_user.id
    )
    return categories
