import pytest
from datetime import datetime
from app.models.user import User, ProviderType
from sqlalchemy.exc import IntegrityError


class TestUserModel:
    """사용자 모델 테스트"""

    def test_create_user_with_github_provider(self, test_db):
        """GitHub 제공자로 사용자 생성 테스트"""
        # Given
        user_data = {
            "email": "github@example.com",
            "username": "githubuser",
            "full_name": "GitHub User",
            "avatar_url": "https://github.com/avatar.jpg",
            "provider": ProviderType.GITHUB,
            "provider_id": "123456",
        }

        # When
        user = User(**user_data)
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        # Then
        assert user.id is not None
        assert user.email == "github@example.com"
        assert user.username == "githubuser"
        assert user.provider == ProviderType.GITHUB
        assert user.provider_id == "123456"
        assert user.is_active is True
        assert user.is_verified is False
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_create_user_with_google_provider(self, test_db):
        """Google 제공자로 사용자 생성 테스트"""
        # Given
        user_data = {
            "email": "google@example.com",
            "username": "googleuser",
            "full_name": "Google User",
            "avatar_url": "https://lh3.googleusercontent.com/avatar.jpg",
            "provider": ProviderType.GOOGLE,
            "provider_id": "789012",
        }

        # When
        user = User(**user_data)
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        # Then
        assert user.id is not None
        assert user.email == "google@example.com"
        assert user.username == "googleuser"
        assert user.provider == ProviderType.GOOGLE
        assert user.provider_id == "789012"

    def test_user_unique_email_constraint(self, test_db):
        """이메일 유니크 제약조건 테스트"""
        # Given
        user1 = User(
            email="duplicate@example.com",
            username="user1",
            provider=ProviderType.GITHUB,
            provider_id="123",
        )
        user2 = User(
            email="duplicate@example.com",  # 중복 이메일
            username="user2",
            provider=ProviderType.GOOGLE,
            provider_id="456",
        )

        # When & Then
        test_db.add(user1)
        test_db.commit()

        test_db.add(user2)
        with pytest.raises(IntegrityError):
            test_db.commit()

    def test_user_unique_username_constraint(self, test_db):
        """사용자명 유니크 제약조건 테스트"""
        # Given
        user1 = User(
            email="user1@example.com",
            username="duplicateuser",
            provider=ProviderType.GITHUB,
            provider_id="123",
        )
        user2 = User(
            email="user2@example.com",
            username="duplicateuser",  # 중복 사용자명
            provider=ProviderType.GOOGLE,
            provider_id="456",
        )

        # When & Then
        test_db.add(user1)
        test_db.commit()

        test_db.add(user2)
        with pytest.raises(IntegrityError):
            test_db.commit()

    def test_user_repr(self, test_db):
        """사용자 모델 __repr__ 메서드 테스트"""
        # Given
        user = User(
            email="test@example.com",
            username="testuser",
            provider=ProviderType.GITHUB,
            provider_id="123",
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        # When
        repr_str = repr(user)

        # Then
        expected = (
            f"<User(id={user.id}, email='test@example.com', provider='github')>"
        )
        assert repr_str == expected

    def test_user_optional_fields(self, test_db):
        """사용자 모델 선택적 필드 테스트"""
        # Given
        user = User(
            email="minimal@example.com",
            username="minimaluser",
            provider=ProviderType.GITHUB,
            provider_id="789",
            # full_name과 avatar_url은 None으로 남겨둠
        )

        # When
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        # Then
        assert user.full_name is None
        assert user.avatar_url is None
        assert user.last_login_at is None
