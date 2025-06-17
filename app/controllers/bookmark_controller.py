from datetime import datetime
from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import HTTPException, status
from app.models.bookmark import BookmarkNote
from app.models.user import User
from app.schemas.bookmark import BookmarkNoteCreate, BookmarkNoteCategoryUpdate
import math


class BookmarkController:
    """북마크 노트 컨트롤러"""

    @staticmethod
    def create_bookmark_note(
        db: Session, bookmark_data: BookmarkNoteCreate, user_id: int
    ) -> BookmarkNote:
        """북마크 노트 생성"""
        # 사용자 존재 확인
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다",
            )

        # 임시로 제목을 URL로 설정 (나중에 AI로 생성할 예정)
        title = f"북마크 - {str(bookmark_data.url)[:50]}..."

        # 북마크 노트 생성
        bookmark_note = BookmarkNote(
            title=title,
            url=str(bookmark_data.url),
            user_id=user_id,
            # 카테고리는 나중에 AI로 생성할 예정
            category1=None,
            category2=None,
            category3=None,
        )

        db.add(bookmark_note)
        db.commit()
        db.refresh(bookmark_note)
        return bookmark_note

    @staticmethod
    def get_bookmark_notes(
        db: Session,
        user_id: int,
        page: int = 1,
        size: int = 20,
        category: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[BookmarkNote], int]:
        """북마크 노트 리스트 조회 (페이지네이션)"""
        query = db.query(BookmarkNote).filter(
            and_(
                BookmarkNote.user_id == user_id,
                BookmarkNote.is_deleted == False,
            )
        )

        # 카테고리 필터링
        if category:
            query = query.filter(
                or_(
                    BookmarkNote.category1.ilike(f"%{category}%"),
                    BookmarkNote.category2.ilike(f"%{category}%"),
                    BookmarkNote.category3.ilike(f"%{category}%"),
                )
            )

        # 검색 필터링
        if search:
            query = query.filter(
                or_(
                    BookmarkNote.title.ilike(f"%{search}%"),
                    BookmarkNote.description.ilike(f"%{search}%"),
                )
            )

        # 총 개수 계산
        total = query.count()

        # 페이지네이션 적용
        offset = (page - 1) * size
        bookmark_notes = (
            query.order_by(BookmarkNote.created_at.desc())
            .offset(offset)
            .limit(size)
            .all()
        )

        return bookmark_notes, total

    @staticmethod
    def get_bookmark_note(
        db: Session, bookmark_id: int, user_id: int
    ) -> BookmarkNote:
        """특정 북마크 노트 조회"""
        bookmark_note = (
            db.query(BookmarkNote)
            .filter(
                and_(
                    BookmarkNote.id == bookmark_id,
                    BookmarkNote.user_id == user_id,
                    BookmarkNote.is_deleted == False,
                )
            )
            .first()
        )

        if not bookmark_note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="북마크 노트를 찾을 수 없습니다",
            )

        return bookmark_note

    @staticmethod
    def update_bookmark_categories(
        db: Session,
        bookmark_id: int,
        user_id: int,
        category_data: BookmarkNoteCategoryUpdate,
    ) -> BookmarkNote:
        """북마크 노트 카테고리 업데이트"""
        bookmark_note = BookmarkController.get_bookmark_note(
            db, bookmark_id, user_id
        )

        # 카테고리 업데이트
        if category_data.category1 is not None:
            bookmark_note.category1 = category_data.category1
        if category_data.category2 is not None:
            bookmark_note.category2 = category_data.category2
        if category_data.category3 is not None:
            bookmark_note.category3 = category_data.category3

        bookmark_note.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(bookmark_note)
        return bookmark_note

    @staticmethod
    def delete_bookmark_note(
        db: Session, bookmark_id: int, user_id: int
    ) -> BookmarkNote:
        """북마크 노트 소프트 삭제"""
        bookmark_note = BookmarkController.get_bookmark_note(
            db, bookmark_id, user_id
        )

        # 소프트 삭제
        bookmark_note.is_deleted = True
        bookmark_note.deleted_at = datetime.utcnow()
        bookmark_note.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(bookmark_note)
        return bookmark_note

    @staticmethod
    def get_categories(db: Session, user_id: int) -> List[str]:
        """사용자의 모든 카테고리 조회"""
        # 각 카테고리 컬럼에서 고유한 값들을 가져와서 합치기
        categories = set()

        # category1에서 가져오기
        cat1_results = (
            db.query(BookmarkNote.category1)
            .filter(
                and_(
                    BookmarkNote.user_id == user_id,
                    BookmarkNote.is_deleted == False,
                    BookmarkNote.category1.isnot(None),
                )
            )
            .distinct()
            .all()
        )

        # category2에서 가져오기
        cat2_results = (
            db.query(BookmarkNote.category2)
            .filter(
                and_(
                    BookmarkNote.user_id == user_id,
                    BookmarkNote.is_deleted == False,
                    BookmarkNote.category2.isnot(None),
                )
            )
            .distinct()
            .all()
        )

        # category3에서 가져오기
        cat3_results = (
            db.query(BookmarkNote.category3)
            .filter(
                and_(
                    BookmarkNote.user_id == user_id,
                    BookmarkNote.is_deleted == False,
                    BookmarkNote.category3.isnot(None),
                )
            )
            .distinct()
            .all()
        )

        # 결과를 set에 추가
        for result in cat1_results:
            if result[0]:
                categories.add(result[0])
        for result in cat2_results:
            if result[0]:
                categories.add(result[0])
        for result in cat3_results:
            if result[0]:
                categories.add(result[0])

        return sorted(list(categories))
