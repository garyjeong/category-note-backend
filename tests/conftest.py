import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.configs.database import get_db, Base
from app.models.user import User
import os
import tempfile

# 테스트 환경 설정
os.environ["TESTING"] = "1"

# 테스트 후 앱 import
from app.main import app

# 테스트용 데이터베이스 URL (SQLite 사용)
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop():
    """이벤트 루프 설정"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def test_db():
    """테스트용 데이터베이스 세션"""
    # SQLite 테스트 데이터베이스 엔진 생성
    engine = create_engine(
        TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )

    # 테이블 생성
    Base.metadata.create_all(bind=engine)

    # 세션 생성
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # 테스트 완료 후 테이블 삭제
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """테스트 클라이언트"""

    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """샘플 사용자 데이터"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "avatar_url": "https://example.com/avatar.jpg",
        "provider": "github",
        "provider_id": "12345",
    }


@pytest.fixture
def github_oauth_response():
    """GitHub OAuth 응답 모킹용 데이터"""
    return {
        "access_token": "gho_test_token",
        "token_type": "bearer",
        "scope": "user:email",
    }


@pytest.fixture
def github_user_api_response():
    """GitHub 사용자 API 응답 모킹용 데이터"""
    return {
        "id": 12345,
        "login": "testuser",
        "name": "Test User",
        "email": "test@example.com",
        "avatar_url": "https://avatars.githubusercontent.com/u/12345",
    }


@pytest.fixture
def github_emails_api_response():
    """GitHub 이메일 API 응답 모킹용 데이터"""
    return [
        {
            "email": "test@example.com",
            "primary": True,
            "verified": True,
            "visibility": "public",
        }
    ]


@pytest.fixture
def google_user_api_response():
    """Google 사용자 API 응답 모킹용 데이터"""
    return {
        "id": "67890",
        "email": "test@gmail.com",
        "name": "Test User",
        "given_name": "Test",
        "picture": "https://lh3.googleusercontent.com/a/test",
    }
