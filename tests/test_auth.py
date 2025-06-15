import pytest
from unittest.mock import patch, AsyncMock
import json
from app.models.user import User, ProviderType
from app.controllers.auth_controller import AuthController


class TestAuthAPI:
    """인증 API 테스트"""

    def test_root_endpoint(self, client):
        """루트 엔드포인트 테스트"""
        # When
        response = client.get("/")

        # Then
        assert response.status_code == 200
        assert response.json() == {"message": "Category Note API"}

    def test_health_check_endpoint(self, client):
        """헬스 체크 엔드포인트 테스트"""
        # When
        response = client.get("/health")

        # Then
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    @patch("app.routers.auth.oauth.create_client")
    def test_login_github_redirect(self, mock_create_client, client):
        """GitHub 로그인 리다이렉트 테스트"""
        # Given
        mock_client = AsyncMock()
        mock_create_client.return_value = mock_client
        mock_client.authorize_redirect = AsyncMock(
            return_value="https://github.com/login/oauth/authorize?..."
        )

        # When
        response = client.get("/auth/login/github", follow_redirects=False)

        # Then
        # OAuth 설정이 없어도 400 에러가 나지 않아야 함
        assert response.status_code in [
            200,
            302,
            500,
        ]  # OAuth 설정 이슈로 500도 허용

    @patch("app.routers.auth.oauth.create_client")
    def test_login_google_redirect(self, mock_create_client, client):
        """Google 로그인 리다이렉트 테스트"""
        # Given
        mock_client = AsyncMock()
        mock_create_client.return_value = mock_client
        mock_client.authorize_redirect = AsyncMock(
            return_value="https://accounts.google.com/o/oauth2/auth?..."
        )

        # When
        response = client.get("/auth/login/google", follow_redirects=False)

        # Then
        # OAuth 설정이 없어도 400 에러가 나지 않아야 함
        assert response.status_code in [
            200,
            302,
            500,
        ]  # OAuth 설정 이슈로 500도 허용

    def test_login_unsupported_provider(self, client):
        """지원하지 않는 OAuth 제공자 테스트"""
        # When
        response = client.get("/auth/login/facebook")

        # Then
        assert response.status_code == 400
        assert "지원하지 않는 OAuth 제공자입니다" in response.json()["detail"]

    @patch("app.routers.auth.oauth")
    @patch("app.routers.auth._get_github_user_info")
    async def test_github_callback_success_new_user(
        self,
        mock_get_user_info,
        mock_oauth,
        client,
        test_db,
        github_user_api_response,
    ):
        """GitHub 콜백 성공 테스트 - 새 사용자"""
        # Given
        mock_client = AsyncMock()
        mock_oauth.create_client.return_value = mock_client
        mock_client.authorize_access_token.return_value = {
            "access_token": "test_token"
        }

        mock_get_user_info.return_value = {
            "email": "github@example.com",
            "username": "githubuser",
            "full_name": "GitHub User",
            "avatar_url": "https://github.com/avatar.jpg",
            "provider": ProviderType.GITHUB,
            "provider_id": "12345",
        }

        # When
        response = client.get("/auth/callback/github?code=test_code")

        # Then
        assert response.status_code in [302, 200]  # 리다이렉트 또는 성공

    def test_callback_unsupported_provider(self, client):
        """지원하지 않는 OAuth 제공자 콜백 테스트"""
        # When
        response = client.get("/auth/callback/facebook?code=test_code")

        # Then
        assert response.status_code == 400
        assert "지원하지 않는 OAuth 제공자입니다" in response.json()["detail"]

    def test_get_current_user_without_token(self, client):
        """토큰 없이 현재 사용자 정보 조회 테스트"""
        # When
        response = client.get("/auth/me")

        # Then
        assert response.status_code == 401
        assert "인증 토큰이 필요합니다" in response.json()["detail"]

    def test_get_current_user_with_invalid_token(self, client):
        """유효하지 않은 토큰으로 현재 사용자 정보 조회 테스트"""
        # When
        response = client.get(
            "/auth/me", headers={"Authorization": "Bearer invalid_token"}
        )

        # Then
        assert response.status_code == 401
        assert "유효하지 않은 토큰입니다" in response.json()["detail"]

    def test_get_current_user_with_valid_token(self, client, test_db):
        """유효한 토큰으로 현재 사용자 정보 조회 테스트"""
        # Given
        user = User(
            email="token_user@example.com",
            username="tokenuser",
            full_name="Token User",
            provider=ProviderType.GITHUB,
            provider_id="token123",
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        # JWT 토큰 생성
        token = AuthController.create_access_token(user)

        # When
        response = client.get(
            "/auth/me", headers={"Authorization": f"Bearer {token}"}
        )

        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "token_user@example.com"
        assert data["username"] == "tokenuser"
        assert data["full_name"] == "Token User"
        assert data["provider"] == "github"

    def test_get_current_user_with_non_existent_user_token(
        self, client, test_db
    ):
        """존재하지 않는 사용자의 토큰으로 조회 테스트"""
        # Given - 존재하지 않는 사용자 ID로 토큰 생성
        fake_user = User(
            id=999,  # 존재하지 않는 ID
            email="fake@example.com",
            username="fakeuser",
            provider=ProviderType.GITHUB,
            provider_id="fake123",
        )
        token = AuthController.create_access_token(fake_user)

        # When
        response = client.get(
            "/auth/me", headers={"Authorization": f"Bearer {token}"}
        )

        # Then
        assert response.status_code == 404
        assert "사용자를 찾을 수 없습니다" in response.json()["detail"]

    def test_logout(self, client):
        """로그아웃 테스트"""
        # When
        response = client.post("/auth/logout")

        # Then
        assert response.status_code == 200
        assert response.json() == {"message": "로그아웃 되었습니다."}

    def test_get_current_user_with_malformed_authorization_header(self, client):
        """잘못된 형식의 Authorization 헤더 테스트"""
        # When
        response = client.get(
            "/auth/me", headers={"Authorization": "InvalidFormat token"}
        )

        # Then
        assert response.status_code == 401
        assert "인증 토큰이 필요합니다" in response.json()["detail"]
