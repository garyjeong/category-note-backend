import os
import sys
from enum import StrEnum
from typing import Dict, Any
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import pymysql.err

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 환경변수 로드 상태를 추적하는 전역 변수
_ENV_LOADED = False


class AppEnv(StrEnum):
    production = "production"
    development = "development"
    testing = "testing"
    local = "local"


def get_current_env() -> str:
    """현재 실행 환경을 반환합니다. 환경변수에서 ENV 또는 APP_ENV가 없으면 development를 기본값으로 사용합니다."""
    return os.getenv("ENV", os.getenv("APP_ENV", "development"))


# 환경변수 한 번만 로드하는 함수
def _load_env_once() -> None:
    global _ENV_LOADED

    if _ENV_LOADED:
        return

    _ENV_LOADED = True
    current_env = get_current_env()

    try:
        # 프로젝트 루트 디렉토리 찾기
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(current_file))
        )

        # 환경별 .env 파일 시도
        env_files = [
            os.path.join(project_root, f".env.{current_env}"),
            os.path.join(project_root, ".env"),
        ]

        env_loaded = False
        for env_file in env_files:
            if os.path.exists(env_file):
                load_dotenv(env_file)
                env_loaded = True
                logger.info(f"환경변수 파일 로드됨: {env_file}")
                break

        if not env_loaded:
            logger.warning(
                f"환경변수 파일을 찾을 수 없습니다. 시도한 파일들: {env_files}"
            )

    except Exception as e:
        logger.error(f"환경변수 로드 중 예외 발생: {str(e)}")


# 프로젝트 시작 시 환경변수 한 번만 로드
_load_env_once()

# 현재 환경 설정
_CURRENT_ENV = get_current_env()


class Configs:
    """기본 설정 클래스. 모든 환경에서 공통으로 사용하는 설정을 정의합니다."""

    APP_ENV: str = _CURRENT_ENV
    DATABASE_USER: str = os.getenv("DATABASE_USER", "category_user")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "category_note")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "3306"))
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "category_password")

    # JWT 설정
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY", "your-secret-key-change-in-production"
    )
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_HOURS: int = int(os.getenv("JWT_EXPIRE_HOURS", "24"))

    # OAuth 설정
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")


class DevelopmentConfigs(Configs):
    """개발 환경 전용 설정 클래스."""

    pass


class TestingConfigs(Configs):
    """테스트 환경 전용 설정 클래스."""

    DATABASE_NAME: str = os.getenv("TEST_DATABASE_NAME", "category_note_test")


class ProductionConfigs(Configs):
    """프로덕션 환경 전용 설정 클래스."""

    # 프로덕션에서는 더 엄격한 설정
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")  # 필수값

    def __post_init__(self):
        if (
            not self.JWT_SECRET_KEY
            or self.JWT_SECRET_KEY == "your-secret-key-change-in-production"
        ):
            raise ValueError(
                "프로덕션 환경에서는 JWT_SECRET_KEY가 반드시 설정되어야 합니다."
            )


def get_database_url() -> str:
    """데이터베이스 접속 URL을 반환합니다."""
    setting = get_configs()
    url = (
        f"mysql+pymysql://{setting.DATABASE_USER}:{setting.DATABASE_PASSWORD}"
        f"@{setting.DATABASE_HOST}:{setting.DATABASE_PORT}/{setting.DATABASE_NAME}"
        f"?charset=utf8mb4"
    )
    # 보안상 패스워드는 로그에 출력하지 않음
    safe_url = url.replace(setting.DATABASE_PASSWORD, "***")
    logger.info(f"데이터베이스 URL: {safe_url}")
    return url


def get_configs():
    """현재 환경에 맞는 설정 객체를 반환합니다."""
    env_mapping = {
        AppEnv.production.value: ProductionConfigs(),
        AppEnv.testing.value: TestingConfigs(),
        AppEnv.development.value: DevelopmentConfigs(),
        AppEnv.local.value: DevelopmentConfigs(),
    }
    return env_mapping.get(_CURRENT_ENV, DevelopmentConfigs())


# 전역 엔진 객체 및 세션 팩토리
_engine = None
_session_factory = None


def get_engine():
    """SQLAlchemy 엔진을 반환합니다. 싱글톤 패턴으로 구현."""
    global _engine
    if _engine is not None:
        return _engine

    url = get_database_url()
    _engine = create_engine(
        url=url,
        pool_pre_ping=True,  # 연결 상태 확인을 위한 ping 활성화
        pool_size=10,  # 기본 풀 사이즈
        max_overflow=20,  # 최대 추가 연결 수
        pool_timeout=60,  # 풀에서 연결을 기다리는 최대 시간(초)
        pool_recycle=3600,  # 1시간마다 연결 재활용
        echo=_CURRENT_ENV
        in [
            AppEnv.development.value,
            AppEnv.local.value,
        ],  # 개발환경에서만 SQL 로깅
        connect_args={
            "connect_timeout": 60,
            "autocommit": False,
        },
    )
    return _engine


def get_session() -> Session:
    """SQLAlchemy 세션을 반환합니다."""
    global _session_factory

    if _session_factory is None:
        engine = get_engine()
        _session_factory = sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    # 세션 생성 시 재시도 로직 추가
    retries = 3
    for attempt in range(retries):
        try:
            session = _session_factory()
            return session
        except Exception as e:
            if attempt < retries - 1:
                logger.warning(
                    f"세션 생성 중 오류 발생, {attempt+1}번째 재시도: {str(e)}"
                )
                import time

                time.sleep(1 * (attempt + 1))  # 지수 백오프 적용
            else:
                logger.error(f"세션 생성 실패: {str(e)}")
                raise


# 안전한 세션 사용을 위한 컨텍스트 매니저
class safe_session:
    """
    DB 연결 실패에 대한 재시도 로직이 포함된 안전한 세션 컨텍스트 매니저.

    예시:
    ```
    with safe_session() as session:
        result = session.execute(query)
        session.commit()
    ```
    """

    def __enter__(self):
        self.session = get_session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                # 예외가 없으면 커밋
                self.session.commit()
            else:
                # 예외가 있으면 롤백
                logger.error(f"세션 예외 발생: {exc_val}")
                self.session.rollback()
        except (pymysql.err.Error, SQLAlchemyError) as e:
            logger.error(f"세션 종료 중 오류: {str(e)}")
            self.session.rollback()
        finally:
            self.session.close()


# 트랜잭션 안전 커밋 함수
def safe_commit(session: Session) -> bool:
    """
    연결이 끊겼을 때 재시도 로직이 포함된 안전한 커밋 함수.

    Args:
        session: 커밋할 Session

    Returns:
        bool: 커밋 성공 여부
    """
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            session.commit()
            return True
        except pymysql.err.Error as e:
            if (
                "MySQL server has gone away" in str(e)
                and retry_count < max_retries - 1
            ):
                retry_count += 1
                logger.warning(
                    f"커밋 실패 (연결 종료), {retry_count}번째 재시도: {str(e)}"
                )
                # 세션 리프레시 시도
                session.close()
                session = get_session()
                import time

                time.sleep(1 * retry_count)  # 지수 백오프
            else:
                logger.error(f"최종 커밋 실패: {str(e)}")
                session.rollback()
                return False
        except SQLAlchemyError as e:
            logger.error(f"커밋 실패 (SQLAlchemy 오류): {str(e)}")
            session.rollback()
            return False
        except Exception as e:
            logger.error(f"커밋 실패 (예상치 못한 오류): {str(e)}")
            session.rollback()
            return False

    return False


# SQLAlchemy Base 클래스
Base = declarative_base()

# 하위 호환성을 위한 기존 변수들
DATABASE_URL = get_database_url()
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 의존성 주입용 함수 (FastAPI에서 사용)
def get_db():
    """FastAPI 의존성 주입용 데이터베이스 세션 생성 함수"""
    with safe_session() as session:
        yield session
