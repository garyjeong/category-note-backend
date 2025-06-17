import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.user import User
from app.controllers.auth_controller import AuthController

client = TestClient(app)


class TestURLAPI:
    """URL API 테스트"""

    @pytest.fixture
    def test_user(self, db_session: Session):
        """테스트용 사용자 생성"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "provider": "github",
            "provider_id": "123456",
        }
        user = AuthController.create_or_update_user(db_session, user_data)
        return user

    @pytest.fixture
    def auth_headers(self, test_user: User):
        """인증 헤더 생성"""
        token = AuthController.create_access_token({"sub": str(test_user.id)})
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def test_url_data(self):
        """테스트용 URL 데이터"""
        return {
            "url": "https://example.com",
            "title": "Example Website",
            "description": "This is an example website",
        }

    def test_create_url_success(
        self, db_session: Session, auth_headers: dict, test_url_data: dict
    ):
        """URL 생성 성공 테스트"""
        response = client.post(
            "/api/url", json=test_url_data, headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["url"] == test_url_data["url"]
        assert data["title"] == test_url_data["title"]
        assert data["description"] == test_url_data["description"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_url_without_auth(self, test_url_data: dict):
        """인증 없이 URL 생성 시도 테스트"""
        response = client.post("/api/url", json=test_url_data)

        assert response.status_code == 401

    def test_create_url_invalid_token(self, test_url_data: dict):
        """잘못된 토큰으로 URL 생성 시도 테스트"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/api/url", json=test_url_data, headers=headers)

        assert response.status_code == 401

    def test_create_url_non_https(self, auth_headers: dict):
        """HTTP URL로 생성 시도 테스트 (HTTPS만 허용)"""
        url_data = {"url": "http://example.com", "title": "HTTP Website"}

        response = client.post("/api/url", json=url_data, headers=auth_headers)

        assert response.status_code == 422  # Validation error

    def test_create_url_invalid_url_format(self, auth_headers: dict):
        """잘못된 URL 형식으로 생성 시도 테스트"""
        url_data = {"url": "not-a-valid-url", "title": "Invalid URL"}

        response = client.post("/api/url", json=url_data, headers=auth_headers)

        assert response.status_code == 422  # Validation error

    def test_create_url_minimal_data(self, auth_headers: dict):
        """최소 데이터로 URL 생성 테스트"""
        url_data = {"url": "https://minimal.com"}

        response = client.post("/api/url", json=url_data, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["url"] == url_data["url"]
        assert data["title"] is None
        assert data["description"] is None
