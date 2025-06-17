# Category Note Backend

YouTube와 지식 웹 페이지를 정리하는 백엔드 API 서비스입니다. TDD(Test-Driven Development) 방식으로 개발되어 안정적이고 신뢰할 수 있는 코드베이스를 제공합니다.

## 📋 목차

- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [프로젝트 구조](#프로젝트-구조)
- [설치 및 실행](#설치-및-실행)
- [테스트](#테스트)
- [API 엔드포인트](#api-엔드포인트)
- [OAuth 설정](#oauth-설정)
- [Docker 사용법](#docker-사용법)
- [개발 가이드](#개발-가이드)
- [환경변수 설정](#환경변수-설정)
- [문제 해결](#문제-해결)

## 🚀 주요 기능

- ✅ **GitHub/Google OAuth 로그인 및 회원가입**
- ✅ **JWT 기반 인증 시스템**
- ✅ **MySQL 데이터베이스 연동**
- ✅ **FastAPI 기반 REST API**
- ✅ **TDD로 개발된 안정적인 코드베이스**
- ✅ **포괄적인 테스트 커버리지 (30+ 테스트)**
- ✅ **Docker 컨테이너 지원**
- ✅ **자동 API 문서화**

## 🛠 기술 스택

### 백엔드
- **FastAPI 0.115.12** - 고성능 웹 프레임워크 (최신 버전)
- **Python 3.9+** - 프로그래밍 언어 (**authlib 1.6.0 호환성으로 인한 최소 버전**)
- **Uvicorn 0.34.3** - ASGI 서버 (최신 버전)
- **uv** - 빠른 Python 패키지 매니저 (pip 대체, 빠른 설치 및 빌드)

### 데이터베이스
- **MySQL 8.0** - 프로덕션 데이터베이스
- **SQLite** - 테스트 환경 데이터베이스
- **SQLAlchemy 2.0.41** - ORM (최신 버전)
- **PyMySQL** - MySQL 드라이버

### 인증
- **OAuth2** - GitHub, Google 소셜 로그인
- **JWT (JSON Web Tokens)** - 토큰 기반 인증
- **Authlib** - OAuth 클라이언트 라이브러리
- **python-jose** - JWT 처리

### 테스트
- **pytest 8.4.0** - 테스트 프레임워크 (최신 버전)
- **pytest-asyncio** - 비동기 테스트 지원
- **pytest-cov 6.2.1** - 코드 커버리지 (최신 버전)
- **factory-boy 3.3.3** - 테스트 데이터 팩토리 (최신 버전)
- **faker 37.4.0** - 가짜 데이터 생성 (최신 버전)

### 개발 도구
- **Docker** - 컨테이너화
- **Pydantic** - 데이터 검증
- **CORS** - 크로스 오리진 요청 지원
- **pyproject.toml** - 현대적인 Python 프로젝트 설정 (uv와 함께)
- **Ruff** - 빠른 린터 및 포매터
- **VS Code 디버그 설정** - 개발 및 테스트 환경 지원

## 📁 프로젝트 구조

```
category-note-backend/
├── app/                          # 메인 애플리케이션
│   ├── __init__.py              # 앱 패키지 초기화
│   ├── main.py                  # FastAPI 애플리케이션 진입점
│   ├── configs/                 # 설정 모듈
│   │   ├── __init__.py         # 설정 패키지 초기화
│   │   ├── database.py         # 데이터베이스 연결 설정
│   │   └── oauth.py            # OAuth 및 JWT 설정
│   ├── models/                  # SQLAlchemy 데이터 모델
│   │   ├── __init__.py         # 모델 패키지 초기화
│   │   └── user.py             # 사용자 모델 (GitHub/Google OAuth 지원)
│   ├── schemas/                 # Pydantic 스키마
│   │   ├── __init__.py         # 스키마 패키지 초기화
│   │   └── user.py             # 사용자 API 스키마
│   ├── controllers/             # 비즈니스 로직
│   │   ├── __init__.py         # 컨트롤러 패키지 초기화
│   │   └── auth_controller.py  # 인증 관련 비즈니스 로직
│   └── routers/                 # API 라우터
│       ├── __init__.py         # 라우터 패키지 초기화
│       └── auth.py             # 인증 API 엔드포인트
├── .vscode/                     # VS Code 설정
│   └── launch.json             # 디버그 설정 (4가지 구성)
├── tests/                       # 테스트 코드 (TDD)
│   ├── __init__.py             # 테스트 패키지 초기화
│   ├── conftest.py             # pytest 설정 및 픽스처
│   ├── test_models.py          # 모델 테스트 (7개 테스트)
│   ├── test_controllers.py     # 컨트롤러 테스트 (12개 테스트)
│   └── test_auth.py            # API 엔드포인트 테스트 (13개 테스트)
├── Dockerfiles/                 # Docker 설정
│   └── database.Dockerfile     # MySQL 컨테이너 설정
├── database/                    # 데이터베이스 설정
│   └── my.cnf                  # MySQL 설정 파일
├── pyproject.toml              # 현대적 Python 프로젝트 설정 (uv, 의존성, 빌드 설정)
├── uv.lock                     # uv 의존성 잠금 파일
├── requirements.txt             # Python 의존성 (레거시)
├── run.py                      # 개발 서버 실행 스크립트
├── test.db                     # SQLite 테스트 데이터베이스 (자동 생성)
└── README.md                   # 프로젝트 문서
```

## 🔧 설치 및 실행

### 1. 저장소 클론

```bash
git clone <repository-url>
cd category-note-backend
```

### 2. uv 설치 (권장)

```bash
# macOS/Linux에서 uv 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 또는 pip로 설치
pip install uv
```

### 3. 의존성 설치

```bash
# uv를 사용하여 가상환경 생성 및 의존성 설치 (권장)
uv sync

# 또는 개발 의존성까지 모두 설치
uv sync --all-groups
```

#### 기존 pip 방식 (레거시)

```bash
# 기존 방식 (권장하지 않음)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 4. 환경변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 환경변수들을 설정하세요:

```env
# 데이터베이스 설정
DATABASE_URL=mysql+pymysql://category_user:category_password@localhost:3306/category_note

# JWT 설정 (보안을 위해 강력한 키 사용)
JWT_SECRET_KEY=your-super-secret-jwt-key-here-make-it-very-long-and-random

# GitHub OAuth 설정
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Google OAuth 설정
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# 서버 설정 (선택사항)
HOST=0.0.0.0
PORT=8000
```

### 5. 데이터베이스 실행

#### Docker를 사용한 MySQL 실행 (권장)

```bash
# MySQL 컨테이너 빌드
docker build -f Dockerfiles/database.Dockerfile -t category-note-db .

# MySQL 컨테이너 실행
docker run -d \
  --name category-note-mysql \
  -p 3306:3306 \
  -v mysql_data:/var/lib/mysql \
  category-note-db

# 컨테이너 상태 확인
docker ps

# 컨테이너 로그 확인
docker logs category-note-mysql
```

#### 로컬 MySQL 사용

로컬에 MySQL이 설치되어 있다면:

```sql
-- MySQL에 접속하여 데이터베이스 생성
CREATE DATABASE category_note CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'category_user'@'localhost' IDENTIFIED BY 'category_password';
GRANT ALL PRIVILEGES ON category_note.* TO 'category_user'@'localhost';
FLUSH PRIVILEGES;
```

### 6. 서버 실행

#### 개발 서버 실행

```bash
# uv를 사용한 실행 (권장)
uv run python run.py

# 또는 uv로 직접 uvicorn 실행
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 기존 방식 (가상환경 활성화 후)
python run.py
# 또는
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 프로덕션 서버 실행

```bash
# uv를 사용한 프로덕션 실행
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# 기존 방식
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

서버가 성공적으로 실행되면 다음 주소에서 접근할 수 있습니다:
- **API 서버**: http://localhost:8000
- **API 문서 (Swagger)**: http://localhost:8000/docs
- **API 문서 (ReDoc)**: http://localhost:8000/redoc

## 🧪 테스트

이 프로젝트는 TDD(Test-Driven Development) 방식으로 개발되어 포괄적인 테스트 커버리지를 제공합니다.

### 전체 테스트 실행

```bash
# uv를 사용한 테스트 실행 (권장)
uv run pytest tests/ -v

# 커버리지와 함께 테스트 실행
uv run pytest tests/ -v --cov=app --cov-report=html

# 특정 테스트 파일만 실행
uv run pytest tests/test_models.py -v
uv run pytest tests/test_controllers.py -v
uv run pytest tests/test_auth.py -v

# 기존 방식 (가상환경 활성화 후)
python -m pytest tests/ -v
python -m pytest tests/ -v --cov=app --cov-report=html
```

### 테스트 카테고리

#### 1. 모델 테스트 (`tests/test_models.py`)
- ✅ GitHub/Google 제공자로 사용자 생성
- ✅ 이메일/사용자명 유니크 제약조건
- ✅ 모델 표현 메서드
- ✅ 선택적 필드 처리

#### 2. 컨트롤러 테스트 (`tests/test_controllers.py`)
- ✅ 사용자 조회 (이메일, OAuth 제공자별)
- ✅ 사용자 생성 및 업데이트
- ✅ JWT 토큰 생성 및 검증
- ✅ 만료된/유효하지 않은 토큰 처리
- ✅ 마지막 로그인 시간 업데이트

#### 3. API 엔드포인트 테스트 (`tests/test_auth.py`)
- ✅ 기본 엔드포인트 (루트, 헬스체크)
- ✅ OAuth 로그인 리다이렉트
- ✅ 현재 사용자 정보 조회
- ✅ JWT 토큰 기반 인증
- ✅ 에러 처리 (잘못된 토큰, 존재하지 않는 사용자)

### 테스트 결과 예시

```
============== test session starts ==============
collected 31 items

tests/test_auth.py::TestAuthAPI::test_root_endpoint PASSED                    [  3%]
tests/test_auth.py::TestAuthAPI::test_health_check_endpoint PASSED           [  6%]
tests/test_auth.py::TestAuthAPI::test_login_github_redirect PASSED           [  9%]
...
tests/test_models.py::TestUserModel::test_user_optional_fields PASSED        [100%]

============== 30 passed, 1 skipped in 0.43s ==============
```

## 🌐 API 엔드포인트

### 기본 엔드포인트

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|------------|------|-----------|
| `GET` | `/` | API 정보 | ❌ |
| `GET` | `/health` | 헬스 체크 | ❌ |

### 인증 관련 엔드포인트

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|------------|------|-----------|
| `GET` | `/auth/login/{provider}` | OAuth 로그인 시작 | ❌ |
| `GET` | `/auth/callback/{provider}` | OAuth 콜백 처리 | ❌ |
| `GET` | `/auth/me` | 현재 사용자 정보 조회 | ✅ |
| `POST` | `/auth/logout` | 로그아웃 | ❌ |

#### 지원되는 OAuth 제공자
- `github` - GitHub OAuth
- `google` - Google OAuth

### API 사용 예시

#### 1. 헬스 체크

```bash
curl -X GET "http://localhost:8000/health"
```

응답:
```json
{
  "status": "healthy"
}
```

#### 2. GitHub 로그인

```bash
# 브라우저에서 접속
http://localhost:8000/auth/login/github
```

#### 3. 현재 사용자 정보 조회

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

응답:
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "User Name",
  "avatar_url": "https://avatars.githubusercontent.com/u/123456",
  "provider": "github",
  "is_active": true,
  "is_verified": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "last_login_at": "2024-01-01T00:00:00"
}
```

## 🔐 OAuth 설정

### GitHub OAuth 앱 생성

1. **GitHub 설정 페이지 접속**
   - https://github.com/settings/developers

2. **새 OAuth 앱 생성**
   - "New OAuth App" 클릭
   - Application name: `Category Note`
   - Homepage URL: `http://localhost:8000`
   - Authorization callback URL: `http://localhost:8000/auth/callback/github`

3. **클라이언트 정보 복사**
   - Client ID와 Client Secret을 `.env` 파일에 추가

### Google OAuth 앱 생성

1. **Google Cloud Console 접속**
   - https://console.cloud.google.com/

2. **프로젝트 생성 또는 선택**

3. **OAuth 동의 화면 설정**
   - APIs & Services > OAuth consent screen
   - User Type: External 선택
   - 필수 정보 입력

4. **OAuth 2.0 클라이언트 ID 생성**
   - APIs & Services > Credentials
   - "Create Credentials" > "OAuth 2.0 Client IDs"
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/auth/callback/google`

5. **클라이언트 정보 복사**
   - Client ID와 Client Secret을 `.env` 파일에 추가

## 🐳 Docker 사용법

### MySQL 데이터베이스 컨테이너

#### 컨테이너 빌드

```bash
docker build -f Dockerfiles/database.Dockerfile -t category-note-db .
```

#### 컨테이너 실행

```bash
# 기본 실행
docker run -d \
  --name category-note-mysql \
  -p 3306:3306 \
  category-note-db

# 환경변수 커스터마이징
docker run -d \
  --name category-note-mysql \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=your_root_password \
  -e MYSQL_DATABASE=your_database_name \
  -e MYSQL_USER=your_username \
  -e MYSQL_PASSWORD=your_password \
  category-note-db

# 데이터 볼륨 마운트 (데이터 영속성)
docker run -d \
  --name category-note-mysql \
  -p 3306:3306 \
  -v mysql_data:/var/lib/mysql \
  category-note-db
```

#### 컨테이너 관리

```bash
# 컨테이너 상태 확인
docker ps

# 컨테이너 로그 확인
docker logs category-note-mysql

# 컨테이너 중지
docker stop category-note-mysql

# 컨테이너 시작
docker start category-note-mysql

# 컨테이너 재시작
docker restart category-note-mysql

# 컨테이너 삭제
docker rm category-note-mysql

# 이미지 삭제
docker rmi category-note-db
```

#### MySQL 컨테이너 접속

```bash
# MySQL 클라이언트로 접속
docker exec -it category-note-mysql mysql -u root -p

# 컨테이너 내부 쉘 접속
docker exec -it category-note-mysql bash
```

### 애플리케이션 Docker화 (선택사항)

애플리케이션도 Docker로 실행하려면 다음 Dockerfile을 생성하세요:

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

빌드 및 실행:

```bash
# 애플리케이션 이미지 빌드
docker build -t category-note-app .

# 애플리케이션 컨테이너 실행
docker run -d \
  --name category-note-app \
  -p 8000:8000 \
  --link category-note-mysql:mysql \
  -e DATABASE_URL=mysql+pymysql://category_user:category_password@mysql:3306/category_note \
  category-note-app
```

### Docker Compose (권장)

전체 스택을 쉽게 관리하려면 `docker-compose.yml` 파일을 생성하세요:

```yaml
version: '3.8'

services:
  mysql:
    build:
      context: .
      dockerfile: Dockerfiles/database.Dockerfile
    container_name: category-note-mysql
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: category_note
      MYSQL_USER: category_user
      MYSQL_PASSWORD: category_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  app:
    build: .
    container_name: category-note-app
    environment:
      DATABASE_URL: mysql+pymysql://category_user:category_password@mysql:3306/category_note
      JWT_SECRET_KEY: your-secret-key
    ports:
      - "8000:8000"
    depends_on:
      - mysql

volumes:
  mysql_data:
```

실행:

```bash
# 전체 스택 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down

# 볼륨까지 삭제
docker-compose down -v
```

## 💻 개발 가이드

### 개발 환경 설정

1. **코드 에디터 설정**
   - VS Code 권장
   - Python 확장 설치
   - 린터 설정 (Ruff 사용)

2. **VS Code 디버그 설정 (.vscode/launch.json)**
   
   프로젝트에 포함된 디버그 설정으로 다음 4가지 구성을 제공합니다:
   
   - **FastAPI Dev Server** - `run.py`를 통한 개발 서버 실행
   - **FastAPI with Uvicorn** - Uvicorn을 직접 사용한 서버 실행
   - **Run Tests** - 테스트 실행 (단순)
   - **Run Tests with Coverage** - 커버리지와 함께 테스트 실행
   
   **사용법**: VS Code에서 `F5` 키를 누르거나 실행 및 디버그 패널에서 원하는 구성을 선택하여 실행

3. **환경변수 설정**
   
   디버그 설정에는 기본 환경변수가 포함되어 있지만, 실제 사용시 `.env` 파일을 생성하여 다음과 같이 설정하세요:
   
   ```env
   DATABASE_URL=mysql+pymysql://category_user:category_password@localhost:3306/category_note
   JWT_SECRET_KEY=your-super-secret-jwt-key-here-make-it-very-long-and-random
   GITHUB_CLIENT_ID=your-github-client-id
   GITHUB_CLIENT_SECRET=your-github-client-secret
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   ```

4. **Git 훅 설정 (선택사항)**
   ```bash
   # pre-commit 설치 (uv 사용)
   uv add --dev pre-commit
   
   # 기존 방식
   pip install pre-commit
   
   # pre-commit 설정
   pre-commit install
   ```

5. **pyproject.toml 설정**
   
   프로젝트는 `pyproject.toml`을 통해 현대적인 Python 프로젝트 구조를 사용합니다:
   
   - **프로젝트 메타데이터**: 이름, 버전, 설명, 저자 정보
   - **의존성 관리**: 프로덕션 및 개발 의존성 분리
   - **빌드 시스템**: Hatchling을 사용한 빌드 설정
   - **테스트 설정**: pytest 구성 및 커버리지 설정
   - **코드 품질**: Ruff 린터 및 포매터 설정
   
   의존성 그룹:
   ```bash
   # 프로덕션 의존성만 설치
   uv sync --only-prod
   
   # 개발 의존성 포함 전체 설치
   uv sync --all-groups
   ```

### 코딩 스타일

- **PEP 8** 준수 (Ruff로 자동 확인)
- **Type hints** 사용
- **Docstring** 작성
- **테스트 우선 개발 (TDD)**
- **Ruff 린터/포매터** 사용 (pyproject.toml에 설정됨)

### 새 기능 추가 시 절차

1. **테스트 작성** (TDD)
   ```bash
   # 테스트 파일 생성
   touch tests/test_new_feature.py
   
   # 실패하는 테스트 작성
   # 기능 구현
   # 테스트 통과 확인
   ```

2. **모델 추가**
   ```python
   # app/models/new_model.py
   from sqlalchemy import Column, Integer, String
   from app.configs.database import Base
   
   class NewModel(Base):
       __tablename__ = "new_table"
       id = Column(Integer, primary_key=True)
       name = Column(String(255))
   ```

3. **스키마 추가**
   ```python
   # app/schemas/new_schema.py
   from pydantic import BaseModel
   
   class NewSchema(BaseModel):
       name: str
   ```

4. **컨트롤러 추가**
   ```python
   # app/controllers/new_controller.py
   class NewController:
       @staticmethod
       def create_item(db, data):
           # 비즈니스 로직
           pass
   ```

5. **라우터 추가**
   ```python
   # app/routers/new_router.py
   from fastapi import APIRouter
   
   router = APIRouter()
   
   @router.post("/items")
   async def create_item():
       pass
   ```

### 데이터베이스 마이그레이션

현재는 SQLAlchemy의 `create_all()`을 사용하지만, 프로덕션에서는 Alembic 사용을 권장합니다:

```bash
# Alembic 설치
pip install alembic

# 초기화
alembic init alembic

# 마이그레이션 생성
alembic revision --autogenerate -m "Add new table"

# 마이그레이션 적용
alembic upgrade head
```

## 🔧 환경변수 설정

### 필수 환경변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `DATABASE_URL` | 데이터베이스 연결 URL | `mysql+pymysql://user:pass@localhost:3306/db` |
| `JWT_SECRET_KEY` | JWT 토큰 서명 키 | `your-super-secret-key` |

### OAuth 환경변수

| 변수명 | 설명 | 획득 방법 |
|--------|------|-----------|
| `GITHUB_CLIENT_ID` | GitHub OAuth 클라이언트 ID | GitHub Developer Settings |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth 클라이언트 시크릿 | GitHub Developer Settings |
| `GOOGLE_CLIENT_ID` | Google OAuth 클라이언트 ID | Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | Google OAuth 클라이언트 시크릿 | Google Cloud Console |

### 선택적 환경변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `HOST` | `0.0.0.0` | 서버 호스트 |
| `PORT` | `8000` | 서버 포트 |
| `TESTING` | - | 테스트 환경 플래그 |

### 환경변수 파일 예시

```env
# .env
# 데이터베이스
DATABASE_URL=mysql+pymysql://category_user:category_password@localhost:3306/category_note

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-make-it-very-long-and-random-for-security

# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# 서버 설정
HOST=0.0.0.0
PORT=8000

# 개발 환경
DEBUG=true
```

## 🔍 문제 해결

### 일반적인 문제들

#### 1. 데이터베이스 연결 오류

**문제**: `Can't connect to MySQL server`

**해결책**:
```bash
# MySQL 컨테이너 상태 확인
docker ps

# MySQL 컨테이너 로그 확인
docker logs category-note-mysql

# MySQL 컨테이너 재시작
docker restart category-note-mysql

# 포트 충돌 확인
lsof -i :3306
```

#### 2. OAuth 설정 오류

**문제**: `404 Not Found for OAuth endpoints`

**해결책**:
- GitHub/Google OAuth 앱 설정 확인
- 콜백 URL이 정확한지 확인
- 클라이언트 ID/Secret이 올바른지 확인

#### 3. JWT 토큰 오류

**문제**: `Invalid token` 오류

**해결책**:
- JWT_SECRET_KEY 환경변수 확인
- 토큰 만료 시간 확인
- 토큰 형식 확인 (`Bearer <token>`)

#### 4. Python 버전 호환성 오류

**문제**: `authlib==1.6.0 depends on Python>=3.9` 오류

**원인**: authlib 1.6.0부터 Python 3.9+ 필요하지만 프로젝트 설정이 >=3.8로 되어 있음

**해결책**:
```bash
# Python 3.9+ 설치 및 사용 확인
python --version  # 3.9 이상이어야 함

# pyproject.toml의 requires-python이 ">=3.9"로 설정되어 있는지 확인
# (이미 업데이트됨)

# uv로 다시 설치
uv sync
```

#### 5. 테스트 실행 오류

**문제**: 테스트가 실행되지 않음

**해결책**:
```bash
# uv를 사용한 테스트 의존성 재설치 (권장)
uv sync --all-groups

# 테스트 환경 확인
uv run python -m pytest --version

# 특정 테스트만 실행
uv run python -m pytest tests/test_models.py -v

# 기존 방식 (레거시)
pip install -r requirements.txt
python -m pytest tests/test_models.py -v
```

### 로그 확인

#### 애플리케이션 로그

```bash
# 개발 서버 실행 시 로그 확인
python run.py

# uvicorn 로그 레벨 설정
uvicorn app.main:app --log-level debug
```

#### Docker 로그

```bash
# MySQL 컨테이너 로그
docker logs category-note-mysql

# 실시간 로그 확인
docker logs -f category-note-mysql
```

### 성능 최적화

#### 데이터베이스 최적화

```sql
-- 인덱스 확인
SHOW INDEX FROM users;

-- 쿼리 성능 분석
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';
```

#### 애플리케이션 최적화

```bash
# 프로덕션 서버 실행 (여러 워커, uv 사용)
uv run uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000

# 기존 방식
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000

# 메모리 사용량 모니터링
uv add --dev memory-profiler
uv run python -m memory_profiler run.py

# 기존 방식
pip install memory-profiler
python -m memory_profiler run.py
```

## 📚 추가 리소스

### 공식 문서
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)
- [pytest 문서](https://docs.pytest.org/)

### 관련 프로젝트
- [FastAPI 보일러플레이트](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- [OAuth 예제](https://github.com/authlib/demo-oauth-client)

### 기여하기

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Implement your changes
5. Ensure all tests pass
6. Submit a pull request

---

**개발자**: Category Note Team  
**라이선스**: MIT  
**버전**: 1.0.0
