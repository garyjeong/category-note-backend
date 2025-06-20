import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# 백엔드 애플리케이션 경로를 Python path에 추가
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 백엔드 애플리케이션의 데이터베이스 설정 가져오기
from app.configs.database import get_database_url, get_configs, AppEnv, Base

# 모든 모델 임포트 (테이블 생성을 위해)
from app.models import user, bookmark, url

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# 현재 환경 설정 가져오기
configs = get_configs()
env = configs.APP_ENV

# 환경별 색상 설정
match env:
    case AppEnv.production.value:
        _color = "[31m"  # 빨간색
    case AppEnv.testing.value:
        _color = "[33m"  # 노란색
    case _:
        _color = "[34m"  # 파란색

color_str = f"\033{_color}{env.upper()}\033[0m"

# 데이터베이스 URL 가져오기 및 설정
database_url = get_database_url()
# 보안상 패스워드는 로그에 출력하지 않음
safe_url = database_url.replace(configs.DATABASE_PASSWORD, "***")
color_url = f"\033{_color}{safe_url}\033[0m"

print(f"[Environment] {color_str} / [URL] {color_url}")
config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 백엔드 애플리케이션의 Base.metadata 사용
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # 타입 변경 감지
        compare_server_default=True,  # 서버 기본값 변경 감지
    )

    with context.begin_transaction():
        context.run_migrations()


def include_object(object, name, type_, reflected, compare_to):
    """마이그레이션에 포함할 객체를 필터링합니다."""
    # 시스템 테이블 제외
    if type_ == "table" and name in [
        "information_schema",
        "performance_schema",
        "mysql",
        "sys",
    ]:
        return False

    # 모든 테이블과 컬럼 포함
    if type_ == "table":
        return True
    if type_ == "column":
        return True
    if type_ == "index":
        return True
    if type_ == "foreign_key":
        return True

    return True


def do_run_migrations(connection) -> None:
    """실제 마이그레이션을 실행합니다."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # 타입 변경 감지
        compare_server_default=True,  # 서버 기본값 변경 감지
        render_as_batch=True,  # MySQL에서 ALTER TABLE을 위한 배치 모드
        include_object=include_object,  # 객체 필터링 함수
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section, {})

    # MySQL 특화 설정
    configuration.setdefault("sqlalchemy.pool_pre_ping", "true")
    configuration.setdefault("sqlalchemy.pool_recycle", "3600")

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    try:
        with connectable.connect() as connection:
            print(f"\033[92m[Database Connection Success!]\033[0m")
            do_run_migrations(connection)
    except Exception as e:
        print(f"\033[91m[Database Connection Failed!]\033[0m Error: {str(e)}")
        raise
    finally:
        connectable.dispose()


def custom_excepthook(type_, value, tb):
    """사용자 정의 예외 처리기"""
    print(f"\nAlembic Error: {value}", file=sys.stderr)


# 사용자 정의 예외 처리기 설정
sys.excepthook = custom_excepthook

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
