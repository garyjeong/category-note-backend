# Category Note Backend

YouTube와 지식 웹 페이지를 정리하는 백엔드 API 서비스입니다. TDD(Test-Driven Development) 방식으로 개발되어 안정적이고 신뢰할 수 있는 코드베이스를 제공합니다.

## 📋 목차

- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [개발 규칙](#개발-규칙)
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
- ✅ **Next.js 프론트엔드 연동**
- ✅ **북마크 노트 관리 시스템**
- ✅ **URL 자동 분석 및 카테고리 분류**

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

## 📏 **개발 규칙**

Category Note 프로젝트는 **직관적 명칭**과 **OOP 설계 원칙**을 기반으로 개발됩니다. 자세한 내용은 **[RULE.md](./RULE.md)**를 참조하세요.

### **핵심 원칙**

#### **1. 직관적 명칭 (Intuitive Naming)**
- ✅ **목적이 명확한 이름**: `create_new_user_account()` vs `create()`
- ✅ **동사 + 명사 조합**: `find_user_by_email_address()`, `validate_user_permissions()`
- ✅ **축약어 금지**: `UserAuthenticationService` vs `UserAuth`
- ✅ **한국어 주석**: `"""새로운 북마크를 생성합니다"""`

#### **2. OOP 설계 원칙**
- ✅ **단일 책임 원칙**: 하나의 클래스는 하나의 책임
- ✅ **의존성 주입**: 추상화에 의존, 구체화에 의존하지 않음
- ✅ **인터페이스 분리**: Repository Pattern 활용
- ✅ **확장 가능한 설계**: Service Layer 구조

### **예시 코드 스타일**

#### **백엔드 (FastAPI)**
```python
class BookmarkManagementService:
    """북마크 관리 비즈니스 로직을 담당하는 서비스"""
    
    def create_new_bookmark(self, user_id: int, bookmark_data: BookmarkCreateDto) -> BookmarkDto:
        """새로운 북마크를 생성합니다"""
        # 비즈니스 로직 구현
        pass
    
    def find_user_bookmarks_by_category(self, user_id: int, category: str) -> List[BookmarkDto]:
        """카테고리별 사용자 북마크 목록을 조회합니다"""
        # 비즈니스 로직 구현
        pass
```

#### **프론트엔드 (Next.js)**
```typescript
class BookmarkApiClient {
    /**
     * 북마크 관련 API 통신을 담당하는 클라이언트
     */
    public async createNewBookmarkNote(bookmarkData: BookmarkCreateRequest): Promise<BookmarkNote> {
        // API 호출 로직
    }
    
    public async fetchUserBookmarkList(userId: number): Promise<BookmarkNote[]> {
        // API 호출 로직
    }
}
```

### **체크리스트**
- [ ] **클래스명**이 역할을 명확히 표현하는가?
- [ ] **메서드명**이 수행하는 액션을 정확히 설명하는가?
- [ ] **변수명**이 저장하는 데이터의 의미를 명확히 전달하는가?
- [ ] **한국어 주석**으로 의도를 명확히 설명했는가?
- [ ] **OOP 원칙**을 준수하여 확장 가능한 구조로 설계했는가?

> **📖 자세한 규칙**: [RULE.md](./RULE.md)에서 전체 개발 가이드라인을 확인하세요.

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
# uv를 사용하여 가상환경 생성 및 의존성 설치
uv sync

# 또는 개발 의존성까지 모두 설치
uv sync --all-groups
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
docker build -f Dockerfiles/database.Dockerfile -t category-note-database .

# MySQL 컨테이너 실행
docker run -d \
  --name category-note-database \
  -p 3306:3306 \
  -v mysql_data:/var/lib/mysql \
  category-note-database

# 컨테이너 상태 확인
docker ps

# 컨테이너 로그 확인
docker logs category-note-database
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
# uv를 사용한 실행
uv run python run.py

# 또는 uv로 직접 uvicorn 실행
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 프로덕션 서버 실행

```bash
# uv를 사용한 프로덕션 실행
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

서버가 성공적으로 실행되면 다음 주소에서 접근할 수 있습니다:
- **API 서버**: http://localhost:8000
- **API 문서 (Swagger)**: http://localhost:8000/docs
- **API 문서 (ReDoc)**: http://localhost:8000/redoc

## 🧪 테스트

이 프로젝트는 TDD(Test-Driven Development) 방식으로 개발되어 포괄적인 테스트 커버리지를 제공합니다.

### 전체 테스트 실행

```bash
# uv를 사용한 테스트 실행
uv run pytest tests/ -v

# 커버리지와 함께 테스트 실행
uv run pytest tests/ -v --cov=app --cov-report=html

# 특정 테스트 파일만 실행
uv run pytest tests/test_models.py -v
uv run pytest tests/test_controllers.py -v
uv run pytest tests/test_auth.py -v
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

#### 4. 북마크 노트 API 테스트 (`tests/test_bookmark.py`)
- ✅ 북마크 노트 생성 (성공, 실패, 유효성 검사)
- ✅ 북마크 노트 목록 조회 (빈 목록, 데이터 있는 목록)
- ✅ 페이지네이션 (페이지 크기, 페이지 번호)
- ✅ 카테고리 필터링 및 검색
- ✅ 특정 북마크 노트 조회 (성공, 404 에러)
- ✅ 북마크 노트 카테고리 수정
- ✅ 북마크 노트 삭제 (소프트 삭제)
- ✅ 카테고리 목록 조회 (중복 제거)
- ✅ 사용자별 데이터 격리

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

### 북마크 노트 관련 엔드포인트

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|------------|------|-----------|
| `POST` | `/api/bookmark/` | 북마크 노트 생성 | ✅ |
| `GET` | `/api/bookmark/` | 북마크 노트 목록 조회 (페이지네이션) | ✅ |
| `GET` | `/api/bookmark/{note_id}` | 특정 북마크 노트 조회 | ✅ |
| `PUT` | `/api/bookmark/{note_id}/categories` | 북마크 노트 카테고리 수정 | ✅ |
| `DELETE` | `/api/bookmark/{note_id}` | 북마크 노트 삭제 (소프트 삭제) | ✅ |
| `GET` | `/api/bookmark/categories/list` | 사용자의 모든 카테고리 목록 조회 | ✅ |

#### 북마크 노트 기능 설명
- **URL 자동 분석**: 북마크 생성 시 URL에서 제목을 자동 추출 (향후 AI 분석 예정)
- **3단계 카테고리**: 각 북마크는 최대 3개의 카테고리를 가질 수 있음
- **소프트 삭제**: 삭제된 북마크는 실제로 삭제되지 않고 `is_deleted` 플래그로 관리
- **사용자별 격리**: 각 사용자는 자신의 북마크만 조회/수정 가능
- **페이지네이션**: 대용량 데이터 처리를 위한 페이지네이션 지원
- **카테고리 필터링**: 특정 카테고리로 북마크 필터링 가능
- **검색 기능**: 제목이나 URL로 북마크 검색 가능

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

#### 4. 북마크 노트 생성

```bash
curl -X POST "http://localhost:8000/api/bookmark/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/interesting-article"
  }'
```

응답:
```json
{
  "id": 1,
  "title": "북마크 - https://example.com/interesting-article...",
  "url": "https://example.com/interesting-article",
  "category1": null,
  "category2": null,
  "category3": null,
  "description": null,
  "user_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "deleted_at": null
}
```

#### 5. 북마크 노트 목록 조회 (페이지네이션)

```bash
curl -X GET "http://localhost:8000/api/bookmark/?page=1&size=10&category=기술&search=FastAPI" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

응답:
```json
{
  "items": [
    {
      "id": 1,
      "title": "FastAPI 완벽 가이드",
      "url": "https://example.com/fastapi-guide",
      "category1": "기술",
      "category2": "웹개발",
      "category3": "Python",
      "description": "FastAPI 프레임워크 학습 자료",
      "user_id": 1,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "deleted_at": null
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

#### 6. 북마크 노트 카테고리 수정

```bash
curl -X PUT "http://localhost:8000/api/bookmark/1/categories" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category1": "기술",
    "category2": "웹개발",
    "category3": "FastAPI"
  }'
```

#### 7. 카테고리 목록 조회

```bash
curl -X GET "http://localhost:8000/api/bookmark/categories/list" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

응답:
```json
["기술", "웹개발", "FastAPI", "Python", "데이터베이스"]
```

## 🌐 프론트엔드 연동

이 백엔드 API는 **Next.js 프론트엔드**와 연동되어 완전한 풀스택 애플리케이션을 제공합니다.

### 프론트엔드 프로젝트
- **위치**: `../category-note-frontend/`
- **기술 스택**: Next.js 15, TypeScript, Tailwind CSS, Zustand, TanStack Query
- **인증 방식**: JWT 토큰 기반 (백엔드와 동일)
- **OAuth 지원**: GitHub/Google 소셜 로그인 완전 연동

### 연동된 기능
- ✅ **OAuth 로그인 플로우**: 백엔드 OAuth 엔드포인트와 완전 연동
- ✅ **JWT 토큰 관리**: 자동 토큰 저장 및 갱신
- ✅ **사용자 인증 상태 관리**: Zustand를 통한 전역 상태 관리
- ✅ **API 클라이언트**: 백엔드 API와의 타입 안전한 통신
- ✅ **2025 트렌드 UI**: Low light mode, Glassmorphism, Micro-interactions 적용

### 개발 환경 실행
```bash
# 백엔드 서버 실행 (포트 8000)
cd category-note-backend
uv run python run.py

# 프론트엔드 개발 서버 실행 (포트 3000)
cd ../category-note-frontend
pnpm dev
```

### CORS 설정
백엔드는 프론트엔드 개발 서버(`http://localhost:3000`)와의 CORS 통신을 허용하도록 설정되어 있습니다.

## 🚀 향후 계획

### 단기 계획 (v1.1)
- [ ] **AI 기반 카테고리 자동 생성**: OpenAI API를 활용하여 URL 분석 후 자동으로 3개 카테고리 생성
- [ ] **URL 메타데이터 자동 추출**: 웹페이지 제목, 설명, 썸네일 이미지 자동 추출
- [ ] **북마크 태그 시스템**: 카테고리 외에 자유로운 태그 추가 기능
- [ ] **북마크 즐겨찾기**: 중요한 북마크를 즐겨찾기로 표시
- [ ] **프론트엔드 북마크 관리 UI**: 북마크 CRUD 인터페이스 완성

### 중기 계획 (v1.2)
- [ ] **전문 검색 엔진**: ElasticSearch 연동으로 고도화된 검색 기능
- [ ] **북마크 공유**: 다른 사용자와 북마크 공유 및 팔로우 기능
- [ ] **북마크 컬렉션**: 관련 북마크들을 그룹화하는 컬렉션 기능
- [ ] **API 키 관리**: 외부 서비스 연동을 위한 API 키 관리
- [ ] **실시간 알림**: WebSocket을 통한 실시간 업데이트

### 장기 계획 (v2.0)
- [ ] **모바일 앱**: React Native 기반 모바일 애플리케이션
- [ ] **브라우저 확장**: Chrome/Firefox 확장 프로그램
- [ ] **AI 추천 시스템**: 사용자 패턴 분석을 통한 개인화된 콘텐츠 추천
- [ ] **소셜 기능**: 커뮤니티, 댓글, 평점 시스템

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



### MySQL 데이터베이스 Docker 설정

프로젝트에 포함된 `Dockerfiles/database.Dockerfile`을 사용하여 MySQL 컨테이너를 구성할 수 있습니다:

#### 데이터베이스 컨테이너 빌드

```bash
# MySQL 컨테이너 이미지 빌드
docker build -f Dockerfiles/database.Dockerfile -t category-note-database .
```

#### 데이터베이스 컨테이너 실행

```bash
# 기본 실행 (환경변수는 Dockerfile에서 설정됨)
docker run -d \
  --name category-note-database \
  -p 3306:3306 \
  -v mysql_data:/var/lib/mysql \
  category-note-database

# 환경변수 커스터마이징 (필요한 경우)
docker run -d \
  --name category-note-database \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=your_root_password \
  -e MYSQL_DATABASE=category_note \
  -e MYSQL_USER=category_user \
  -e MYSQL_PASSWORD=your_password \
  -v mysql_data:/var/lib/mysql \
  category-note-database
```

#### 컨테이너 관리

```bash
# 컨테이너 상태 확인
docker ps

# 컨테이너 로그 확인
docker logs category-note-database

# 컨테이너 중지
docker stop category-note-database

# 컨테이너 시작
docker start category-note-database

# 컨테이너 재시작
docker restart category-note-database

# 컨테이너 삭제
docker rm category-note-database

# 이미지 삭제
docker rmi category-note-database
```

#### MySQL 컨테이너 접속

```bash
# MySQL 클라이언트로 접속
docker exec -it category-note-database mysql -u root -p

# 컨테이너 내부 쉘 접속
docker exec -it category-note-database bash
```

### 데이터베이스 연결 확인

MySQL 컨테이너가 정상적으로 실행된 후, 애플리케이션에서 데이터베이스 연결을 확인할 수 있습니다:

```bash
# 환경변수 설정 (MySQL 컨테이너와 일치해야 함)
export DATABASE_URL="mysql+pymysql://user:wjdwhdans@localhost:3306/category_note"

# Alembic으로 데이터베이스 연결 테스트
uv run alembic current

# 애플리케이션 실행
uv run python run.py
```

**참고**: `Dockerfiles/database.Dockerfile`에 설정된 기본 환경변수:
- `MYSQL_ROOT_PASSWORD`: `wjdwhdans`
- `MYSQL_DATABASE`: `category_note`
- `MYSQL_USER`: `user`
- `MYSQL_PASSWORD`: `wjdwhdans`

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
   # pre-commit 설치
   uv add --dev pre-commit
   
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
# Alembic 초기화
uv run alembic init alembic

# 마이그레이션 생성 (자동 생성)
uv run alembic revision --autogenerate -m "Add new table"

# 마이그레이션 생성 (특정 rev-id 지정)
uv run alembic revision --autogenerate --rev-id "001" -m "Initial migration"

# 마이그레이션 생성 (수동 생성)
uv run alembic revision --rev-id "002" -m "Custom migration"

# 마이그레이션 적용
uv run alembic upgrade head

# 특정 버전으로 업그레이드
uv run alembic upgrade 001

# 마이그레이션 히스토리 확인
uv run alembic history

# 현재 버전 확인
uv run alembic current
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

#### 4. MySQL 연결 오류 (가장 흔한 문제)

**문제**: `Can't connect to MySQL server on 'localhost'` 오류

**원인**: MySQL 서버가 실행되지 않음

**해결책**:
```bash
# database.Dockerfile을 사용하여 MySQL 컨테이너 빌드
docker build -f Dockerfiles/database.Dockerfile -t category-note-database .

# MySQL 컨테이너 실행
docker run -d \
  --name category-note-database \
  -p 3306:3306 \
  -v mysql_data:/var/lib/mysql \
  category-note-database

# 연결 테스트
uv run alembic current
```

#### 5. 환경변수 파일 누락

**문제**: 환경변수 파일을 찾을 수 없다는 경고

**해결책**:
```bash
# .env 파일 생성 (database.Dockerfile 환경변수와 일치)
cat > .env << 'EOF'
DATABASE_URL=mysql+pymysql://user:wjdwhdans@localhost:3306/category_note
JWT_SECRET_KEY=your-super-secret-jwt-key-here-make-it-very-long-and-random
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
EOF
```

#### 6. Python 버전 호환성 오류

**문제**: `authlib==1.6.0 depends on Python>=3.9` 오류

**원인**: authlib 1.6.0부터 Python 3.9+ 필요

**해결책**:
```bash
# Python 3.9+ 설치 및 사용 확인
python --version  # 3.9 이상이어야 함

# uv로 다시 설치
uv sync
```

#### 7. 테스트 실행 오류

**문제**: 테스트가 실행되지 않음

**해결책**:
```bash
# uv를 사용한 테스트 의존성 재설치
uv sync --all-groups

# 테스트 환경 확인
uv run python -m pytest --version

# 특정 테스트만 실행
uv run python -m pytest tests/test_models.py -v
```

#### 8. Docker 빌드 오류

**문제**: MySQL Docker 이미지 빌드 실패

**해결책**:
```bash
# .dockerignore 파일이 존재하는지 확인 (.venv 제외)
cat .dockerignore

# 캐시 없이 빌드
docker build --no-cache -f Dockerfiles/database.Dockerfile -t category-note-database .

# 빌드 과정 상세 로그 확인
docker build -f Dockerfiles/database.Dockerfile -t category-note-database . --progress=plain
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
# 프로덕션 서버 실행 (여러 워커)
uv run uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000

# 메모리 사용량 모니터링
uv add --dev memory-profiler
uv run python -m memory_profiler run.py
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
