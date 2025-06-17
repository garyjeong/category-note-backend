import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app

# 모든 모델을 import (SQLAlchemy 관계 설정을 위해)
from app.models import user, url, bookmark
from app.models.bookmark import BookmarkNote
from app.models.user import User, ProviderType
from app.controllers.auth_controller import AuthController
from app.schemas.user import OAuthUserInfo
from tests.conftest import test_db


class TestBookmarkAPI:
    """북마크 노트 API 테스트"""

    @pytest.fixture
    def test_user(self, test_db: Session):
        """테스트용 사용자 생성"""
        user_data = OAuthUserInfo(
            email="bookmark_test@example.com",
            username="bookmark_user",
            full_name="Bookmark Test User",
            provider=ProviderType.GITHUB,
            provider_id="bookmark123",
        )
        user = AuthController.create_user(test_db, user_data)
        return user

    @pytest.fixture
    def auth_headers(self, test_user: User):
        """인증 헤더 생성"""
        token = AuthController.create_access_token(test_user)
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def sample_bookmark_data(self):
        """샘플 북마크 데이터"""
        return {"url": "https://example.com/test-article"}

    def test_create_bookmark_note_success(
        self,
        client,
        test_db: Session,
        auth_headers: dict,
        sample_bookmark_data: dict,
    ):
        """북마크 노트 생성 성공 테스트"""
        response = client.post(
            "/api/bookmark/", json=sample_bookmark_data, headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["url"] == sample_bookmark_data["url"]
        assert data["title"].startswith("북마크 -")
        assert data["user_id"] is not None
        assert data["created_at"] is not None

    def test_create_bookmark_note_unauthorized(
        self, client, sample_bookmark_data: dict
    ):
        """인증되지 않은 사용자의 북마크 노트 생성 실패 테스트"""
        response = client.post("/api/bookmark/", json=sample_bookmark_data)

        assert response.status_code == 401

    def test_create_bookmark_note_invalid_url(self, client, auth_headers: dict):
        """잘못된 URL로 북마크 노트 생성 실패 테스트"""
        invalid_data = {"url": "http://example.com"}  # HTTP는 허용되지 않음

        response = client.post(
            "/api/bookmark/", json=invalid_data, headers=auth_headers
        )

        assert response.status_code == 422  # Validation error

    def test_get_bookmark_notes_empty(self, client, auth_headers: dict):
        """빈 북마크 노트 리스트 조회 테스트"""
        response = client.get("/api/bookmark/", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["size"] == 20  # 기본 페이지 크기

    def test_get_bookmark_notes_with_data(
        self, client, test_db: Session, test_user: User, auth_headers: dict
    ):
        """데이터가 있는 북마크 노트 리스트 조회 테스트"""
        # 테스트 데이터 생성
        bookmark1 = BookmarkNote(
            title="테스트 북마크 1",
            url="https://example.com/1",
            category1="기술",
            category2="프로그래밍",
            user_id=test_user.id,
        )
        bookmark2 = BookmarkNote(
            title="테스트 북마크 2",
            url="https://example.com/2",
            category1="디자인",
            user_id=test_user.id,
        )
        test_db.add_all([bookmark1, bookmark2])
        test_db.commit()

        response = client.get("/api/bookmark/", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 2

    def test_get_bookmark_notes_pagination(
        self, client, test_db: Session, test_user: User, auth_headers: dict
    ):
        """페이지네이션 테스트"""
        # 5개의 테스트 데이터 생성
        for i in range(5):
            bookmark = BookmarkNote(
                title=f"테스트 북마크 {i+1}",
                url=f"https://example.com/{i+1}",
                user_id=test_user.id,
            )
            test_db.add(bookmark)
        test_db.commit()

        # 첫 번째 페이지 (크기: 2)
        response = client.get(
            "/api/bookmark/?page=1&size=2", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["size"] == 2
        assert data["pages"] == 3  # 실제 응답 필드명

    def test_get_bookmark_notes_category_filter(
        self, client, test_db: Session, test_user: User, auth_headers: dict
    ):
        """카테고리 필터링 테스트"""
        # 다른 카테고리의 북마크 생성
        bookmark1 = BookmarkNote(
            title="기술 북마크",
            url="https://example.com/tech",
            category1="기술",
            user_id=test_user.id,
        )
        bookmark2 = BookmarkNote(
            title="디자인 북마크",
            url="https://example.com/design",
            category1="디자인",
            user_id=test_user.id,
        )
        test_db.add_all([bookmark1, bookmark2])
        test_db.commit()

        response = client.get(
            "/api/bookmark/?category=기술", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["category1"] == "기술"

    def test_get_bookmark_note_by_id(
        self, client, test_db: Session, test_user: User, auth_headers: dict
    ):
        """특정 북마크 노트 조회 테스트"""
        bookmark = BookmarkNote(
            title="특정 북마크",
            url="https://example.com/specific",
            user_id=test_user.id,
        )
        test_db.add(bookmark)
        test_db.commit()
        test_db.refresh(bookmark)

        response = client.get(
            f"/api/bookmark/{bookmark.id}", headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == bookmark.id
        assert data["title"] == bookmark.title

    def test_get_bookmark_note_not_found(self, client, auth_headers: dict):
        """존재하지 않는 북마크 노트 조회 테스트"""
        response = client.get("/api/bookmark/999", headers=auth_headers)

        assert response.status_code == 404

    def test_update_bookmark_categories(
        self, client, test_db: Session, test_user: User, auth_headers: dict
    ):
        """북마크 노트 카테고리 업데이트 테스트"""
        bookmark = BookmarkNote(
            title="업데이트 테스트",
            url="https://example.com/update",
            user_id=test_user.id,
        )
        test_db.add(bookmark)
        test_db.commit()
        test_db.refresh(bookmark)

        update_data = {
            "category1": "새로운 카테고리1",
            "category2": "새로운 카테고리2",
            "category3": "새로운 카테고리3",
        }

        response = client.put(
            f"/api/bookmark/{bookmark.id}/categories",
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["category1"] == "새로운 카테고리1"
        assert data["category2"] == "새로운 카테고리2"
        assert data["category3"] == "새로운 카테고리3"

    def test_delete_bookmark_note(
        self, client, test_db: Session, test_user: User, auth_headers: dict
    ):
        """북마크 노트 삭제 테스트"""
        bookmark = BookmarkNote(
            title="삭제 테스트",
            url="https://example.com/delete",
            user_id=test_user.id,
        )
        test_db.add(bookmark)
        test_db.commit()
        test_db.refresh(bookmark)

        response = client.delete(
            f"/api/bookmark/{bookmark.id}", headers=auth_headers
        )

        assert response.status_code == 200

        # 삭제 후 조회 시 404 반환 확인
        get_response = client.get(
            f"/api/bookmark/{bookmark.id}", headers=auth_headers
        )
        assert get_response.status_code == 404

    def test_get_categories(
        self, client, test_db: Session, test_user: User, auth_headers: dict
    ):
        """카테고리 목록 조회 테스트"""
        # 다양한 카테고리의 북마크 생성
        bookmarks = [
            BookmarkNote(
                title="북마크 1",
                url="https://example.com/1",
                category1="기술",
                category2="프로그래밍",
                user_id=test_user.id,
            ),
            BookmarkNote(
                title="북마크 2",
                url="https://example.com/2",
                category1="디자인",
                category3="UI/UX",
                user_id=test_user.id,
            ),
            BookmarkNote(
                title="북마크 3",
                url="https://example.com/3",
                category2="프로그래밍",  # 중복 카테고리
                user_id=test_user.id,
            ),
        ]
        test_db.add_all(bookmarks)
        test_db.commit()

        response = client.get(
            "/api/bookmark/categories/list", headers=auth_headers
        )

        assert response.status_code == 200
        categories = response.json()  # 직접 리스트 반환
        assert "기술" in categories
        assert "디자인" in categories
        assert "프로그래밍" in categories
        assert "UI/UX" in categories
        # 중복 제거 확인
        assert categories.count("프로그래밍") == 1

    def test_user_isolation(self, client, test_db: Session, auth_headers: dict):
        """사용자별 데이터 격리 테스트"""
        # 다른 사용자 생성
        other_user_data = OAuthUserInfo(
            email="other@example.com",
            username="other_user",
            provider=ProviderType.GOOGLE,
            provider_id="other123",
        )
        other_user = AuthController.create_user(test_db, other_user_data)

        # 다른 사용자의 북마크 생성
        other_bookmark = BookmarkNote(
            title="다른 사용자 북마크",
            url="https://example.com/other",
            user_id=other_user.id,
        )
        test_db.add(other_bookmark)
        test_db.commit()

        # 현재 사용자는 다른 사용자의 북마크를 볼 수 없어야 함
        response = client.get("/api/bookmark/", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0  # 다른 사용자의 북마크는 보이지 않음
