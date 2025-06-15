import pytest
from datetime import datetime, timedelta
from jose import jwt
from app.controllers.auth_controller import AuthController
from app.models.user import User, ProviderType
from app.schemas.user import OAuthUserInfo
from app.configs.oauth import JWT_SECRET_KEY, JWT_ALGORITHM


class TestAuthController:
    """인증 컨트롤러 테스트"""

    def test_get_user_by_email_existing_user(self, test_db):
        """이메일로 기존 사용자 조회 테스트"""
        # Given
        user = User(
            email="existing@example.com",
            username="existinguser",
            provider=ProviderType.GITHUB,
            provider_id="123",
        )
        test_db.add(user)
        test_db.commit()

        # When
        found_user = AuthController.get_user_by_email(
            test_db, "existing@example.com"
        )

        # Then
        assert found_user is not None
        assert found_user.email == "existing@example.com"
        assert found_user.username == "existinguser"

    def test_get_user_by_email_non_existing_user(self, test_db):
        """이메일로 존재하지 않는 사용자 조회 테스트"""
        # When
        found_user = AuthController.get_user_by_email(
            test_db, "nonexistent@example.com"
        )

        # Then
        assert found_user is None

    def test_get_user_by_provider_existing_user(self, test_db):
        """OAuth 제공자로 기존 사용자 조회 테스트"""
        # Given
        user = User(
            email="github_user@example.com",
            username="githubuser",
            provider=ProviderType.GITHUB,
            provider_id="github123",
        )
        test_db.add(user)
        test_db.commit()

        # When
        found_user = AuthController.get_user_by_provider(
            test_db, ProviderType.GITHUB, "github123"
        )

        # Then
        assert found_user is not None
        assert found_user.provider == ProviderType.GITHUB
        assert found_user.provider_id == "github123"

    def test_get_user_by_provider_non_existing_user(self, test_db):
        """OAuth 제공자로 존재하지 않는 사용자 조회 테스트"""
        # When
        found_user = AuthController.get_user_by_provider(
            test_db, ProviderType.GITHUB, "nonexistent123"
        )

        # Then
        assert found_user is None

    def test_create_user(self, test_db):
        """새 사용자 생성 테스트"""
        # Given
        oauth_user = OAuthUserInfo(
            email="new@example.com",
            username="newuser",
            full_name="New User",
            avatar_url="https://example.com/avatar.jpg",
            provider=ProviderType.GITHUB,
            provider_id="new123",
        )

        # When
        created_user = AuthController.create_user(test_db, oauth_user)

        # Then
        assert created_user.id is not None
        assert created_user.email == "new@example.com"
        assert created_user.username == "newuser"
        assert created_user.full_name == "New User"
        assert created_user.avatar_url == "https://example.com/avatar.jpg"
        assert created_user.provider == ProviderType.GITHUB
        assert created_user.provider_id == "new123"
        assert created_user.is_verified is True  # OAuth 사용자는 기본 인증됨

    def test_update_last_login(self, test_db):
        """마지막 로그인 시간 업데이트 테스트"""
        # Given
        user = User(
            email="login@example.com",
            username="loginuser",
            provider=ProviderType.GITHUB,
            provider_id="login123",
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        initial_login_time = user.last_login_at

        # When
        updated_user = AuthController.update_last_login(test_db, user)

        # Then
        assert updated_user.last_login_at is not None
        assert updated_user.last_login_at != initial_login_time
        assert isinstance(updated_user.last_login_at, datetime)

    def test_create_access_token(self, test_db):
        """JWT 액세스 토큰 생성 테스트"""
        # Given
        user = User(
            id=1,
            email="token@example.com",
            username="tokenuser",
            provider=ProviderType.GITHUB,
            provider_id="token123",
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        # When
        token = AuthController.create_access_token(user)

        # Then
        assert token is not None
        assert isinstance(token, str)

        # 토큰 디코딩하여 내용 확인
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        assert payload["user_id"] == user.id
        assert payload["email"] == user.email
        assert "exp" in payload

    def test_verify_valid_token(self, test_db):
        """유효한 JWT 토큰 검증 테스트"""
        # Given
        user = User(
            id=1,
            email="verify@example.com",
            username="verifyuser",
            provider=ProviderType.GITHUB,
            provider_id="verify123",
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        token = AuthController.create_access_token(user)

        # When
        payload = AuthController.verify_token(token)

        # Then
        assert payload is not None
        assert payload["user_id"] == user.id
        assert payload["email"] == user.email

    def test_verify_expired_token(self):
        """만료된 JWT 토큰 검증 테스트"""
        # Given - 만료된 토큰 생성
        expired_payload = {
            "user_id": 1,
            "email": "expired@example.com",
            "exp": datetime.utcnow() - timedelta(seconds=1),  # 1초 전에 만료
        }
        expired_token = jwt.encode(
            expired_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
        )

        # When
        payload = AuthController.verify_token(expired_token)

        # Then
        assert payload is None

    def test_verify_invalid_token(self):
        """유효하지 않은 JWT 토큰 검증 테스트"""
        # Given
        invalid_token = "invalid.token.here"

        # When
        payload = AuthController.verify_token(invalid_token)

        # Then
        assert payload is None

    def test_get_or_create_user_existing_user(self, test_db):
        """기존 사용자 조회 또는 생성 테스트 - 기존 사용자"""
        # Given
        existing_user = User(
            email="existing@example.com",
            username="existinguser",
            full_name="Old Name",
            avatar_url="https://old-avatar.com",
            provider=ProviderType.GITHUB,
            provider_id="existing123",
        )
        test_db.add(existing_user)
        test_db.commit()
        test_db.refresh(existing_user)

        oauth_user = OAuthUserInfo(
            email="existing@example.com",
            username="existinguser",
            full_name="Updated Name",
            avatar_url="https://new-avatar.com",
            provider=ProviderType.GITHUB,
            provider_id="existing123",
        )

        # When
        user = AuthController.get_or_create_user(test_db, oauth_user)

        # Then
        assert user.id == existing_user.id
        assert user.full_name == "Updated Name"  # 업데이트됨
        assert user.avatar_url == "https://new-avatar.com"  # 업데이트됨

    def test_get_or_create_user_new_user(self, test_db):
        """기존 사용자 조회 또는 생성 테스트 - 새 사용자"""
        # Given
        oauth_user = OAuthUserInfo(
            email="new@example.com",
            username="newuser",
            full_name="New User",
            avatar_url="https://new-avatar.com",
            provider=ProviderType.GOOGLE,
            provider_id="new123",
        )

        # When
        user = AuthController.get_or_create_user(test_db, oauth_user)

        # Then
        assert user.id is not None
        assert user.email == "new@example.com"
        assert user.username == "newuser"
        assert user.provider == ProviderType.GOOGLE
        assert user.provider_id == "new123"
        assert user.is_verified is True
