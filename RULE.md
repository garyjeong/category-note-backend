# Category Note 개발 규칙 (RULE.md)

## 📋 목차

- [핵심 원칙](#핵심-원칙)
- [명칭 규칙](#명칭-규칙)
- [OOP 설계 원칙](#oop-설계-원칙)
- [백엔드 규칙](#백엔드-규칙)
- [프론트엔드 규칙](#프론트엔드-규칙)
- [공통 코딩 스타일](#공통-코딩-스타일)
- [테스트 규칙](#테스트-규칙)

---

## 🎯 **핵심 원칙**

### **1. 직관적 명칭 (Intuitive Naming)**
```
✅ 목적이 명확하게 드러나는 이름 사용
✅ 축약어보다는 풀네임 선호
✅ 동사 + 명사 조합으로 액션 표현
✅ 한국어 주석으로 의도 명시
```

### **2. OOP 설계 원칙 (Object-Oriented Design)**
```
✅ 단일 책임 원칙 (SRP): 하나의 클래스는 하나의 책임
✅ 개방-폐쇄 원칙 (OCP): 확장에는 열려있고 수정에는 닫혀있게
✅ 의존성 역전 원칙 (DIP): 추상화에 의존, 구체화에 의존하지 않음
✅ 인터페이스 분리 원칙 (ISP): 클라이언트는 자신이 사용하지 않는 메서드에 의존하지 않음
```

---

## 🏷️ **명칭 규칙**

### **백엔드 (Python)**

#### **클래스명**
```python
✅ PascalCase + 역할 접미사
class UserAuthenticationService:     # 서비스
class BookmarkDataRepository:        # 저장소
class AuthenticationController:      # 컨트롤러
class BookmarkNoteValidator:         # 검증자

❌ 피할 것
class UserAuth:                      # 축약어
class Data:                          # 추상적
class Utils:                         # 역할 불명확
```

#### **메서드명**
```python
✅ 동사 + 명사 조합 (snake_case)
def create_new_user_account():       # 생성 액션
def find_user_by_email_address():   # 조회 액션
def update_bookmark_content():       # 수정 액션
def validate_user_permissions():     # 검증 액션
def calculate_bookmark_statistics(): # 계산 액션

❌ 피할 것
def get_user():                      # 너무 단순
def process():                       # 추상적
def handle():                        # 역할 불명확
```

#### **변수명**
```python
✅ 명확한 의미 전달 (snake_case)
user_authentication_token = "..."
bookmark_creation_timestamp = datetime.now()
email_validation_result = True
oauth_provider_configuration = {...}

❌ 피할 것
token = "..."                        # 어떤 토큰인지 불명확
data = {...}                         # 너무 추상적
result = True                        # 무엇의 결과인지 불명확
```

### **프론트엔드 (TypeScript)**

#### **클래스명**
```typescript
✅ PascalCase + 역할 접미사
class BookmarkApiClient              // API 클라이언트
class UserAuthenticationManager     // 인증 관리자
class BookmarkNotificationService   // 알림 서비스
class CategoryFilterComponent       // 컴포넌트

❌ 피할 것
class ApiClient                     // 어떤 API인지 불명확
class Manager                       // 무엇을 관리하는지 불명확
```

#### **함수/메서드명**
```typescript
✅ 동사 + 명사 조합 (camelCase)
const createNewBookmarkNote = () => {}
const fetchUserBookmarkList = () => {}
const validateEmailAddress = () => {}
const handleUserLoginSuccess = () => {}
const calculateBookmarkScore = () => {}

❌ 피할 것
const create = () => {}             // 무엇을 생성하는지 불명확
const handle = () => {}             // 무엇을 처리하는지 불명확
```

#### **변수명**
```typescript
✅ 명확한 의미 전달 (camelCase)
const userAuthenticationToken = localStorage.getItem('token')
const bookmarkCreationForm = useForm()
const currentUserProfile = useAuthStore(state => state.user)
const categoryFilterOptions = ['tech', 'design', 'business']

❌ 피할 것
const token = localStorage.getItem('token')    // 어떤 토큰인지 불명확
const form = useForm()                        // 어떤 폼인지 불명확
```

---

## 🏗️ **OOP 설계 원칙**

### **백엔드 구조**

#### **1. 서비스 계층 (Service Layer)**
```python
class BookmarkManagementService:
    """북마크 관리 비즈니스 로직을 담당하는 서비스"""
    
    def __init__(self, repository: BookmarkRepository):
        self._repository = repository
    
    def create_new_bookmark(self, user_id: int, bookmark_data: BookmarkCreateDto) -> BookmarkDto:
        """새로운 북마크를 생성합니다"""
        # 비즈니스 로직 구현
        pass
    
    def find_user_bookmarks(self, user_id: int, filter_options: FilterOptions) -> List[BookmarkDto]:
        """사용자의 북마크 목록을 조회합니다"""
        # 비즈니스 로직 구현
        pass
```

#### **2. 저장소 패턴 (Repository Pattern)**
```python
from abc import ABC, abstractmethod

class BookmarkRepository(ABC):
    """북마크 저장소 인터페이스"""
    
    @abstractmethod
    def save_bookmark(self, bookmark: Bookmark) -> Bookmark:
        """북마크를 저장합니다"""
        pass
    
    @abstractmethod
    def find_bookmark_by_id(self, bookmark_id: int) -> Optional[Bookmark]:
        """ID로 북마크를 조회합니다"""
        pass

class DatabaseBookmarkRepository(BookmarkRepository):
    """데이터베이스 기반 북마크 저장소 구현"""
    
    def save_bookmark(self, bookmark: Bookmark) -> Bookmark:
        # SQLAlchemy 구현
        pass
```

#### **3. 컨트롤러 계층 (Controller Layer)**
```python
class BookmarkController:
    """북마크 API 컨트롤러"""
    
    def __init__(self, service: BookmarkManagementService):
        self._service = service
    
    async def create_bookmark_endpoint(self, request: BookmarkCreateRequest) -> BookmarkResponse:
        """북마크 생성 API 엔드포인트"""
        # HTTP 요청/응답 처리
        pass
```

### **프론트엔드 구조**

#### **1. 상태 관리 클래스**
```typescript
class BookmarkStateManager {
  /**
   * 북마크 상태를 관리하는 클래스
   */
  private bookmarks: BookmarkNote[] = []
  private isLoading: boolean = false
  
  public createNewBookmark(bookmarkData: BookmarkCreateData): Promise<BookmarkNote> {
    // 북마크 생성 로직
  }
  
  public fetchUserBookmarks(userId: number): Promise<BookmarkNote[]> {
    // 북마크 조회 로직
  }
  
  public updateBookmarkContent(bookmarkId: number, content: string): Promise<BookmarkNote> {
    // 북마크 업데이트 로직
  }
}
```

#### **2. API 클라이언트 클래스**
```typescript
class BookmarkApiClient {
  /**
   * 북마크 관련 API 통신을 담당하는 클라이언트
   */
  private readonly baseUrl: string
  private readonly httpClient: HttpClient
  
  constructor(baseUrl: string, httpClient: HttpClient) {
    this.baseUrl = baseUrl
    this.httpClient = httpClient
  }
  
  public async createBookmarkNote(bookmarkData: BookmarkCreateRequest): Promise<BookmarkNote> {
    // API 호출 로직
  }
  
  public async fetchBookmarkList(pagination: PaginationOptions): Promise<BookmarkListResponse> {
    // API 호출 로직
  }
}
```

#### **3. 컴포넌트 클래스 설계**
```typescript
interface BookmarkFormProps {
  onBookmarkCreate: (bookmark: BookmarkNote) => void
  initialData?: BookmarkNote
}

class BookmarkFormComponent implements React.FC<BookmarkFormProps> {
  /**
   * 북마크 생성/수정 폼 컴포넌트
   */
  
  private validateBookmarkData(data: BookmarkFormData): ValidationResult {
    // 폼 데이터 검증
  }
  
  private handleFormSubmission = async (formData: BookmarkFormData): Promise<void> => {
    // 폼 제출 처리
  }
  
  public render(): JSX.Element {
    // 렌더링 로직
  }
}
```

---

## 🔧 **백엔드 규칙**

### **1. 파일 구조**
```
app/
├── services/           # 비즈니스 로직 서비스
├── repositories/       # 데이터 저장소
├── controllers/        # API 컨트롤러
├── models/            # 데이터 모델
├── schemas/           # 검증 스키마
├── validators/        # 커스텀 검증자
└── exceptions/        # 커스텀 예외
```

### **2. 의존성 주입 패턴**
```python
# 의존성 주입을 위한 컨테이너
class DependencyContainer:
    def create_bookmark_service(self) -> BookmarkManagementService:
        repository = self.create_bookmark_repository()
        return BookmarkManagementService(repository)
    
    def create_bookmark_repository(self) -> BookmarkRepository:
        return DatabaseBookmarkRepository(self.database_session)
```

### **3. 예외 처리**
```python
class BookmarkNotFoundException(Exception):
    """북마크를 찾을 수 없을 때 발생하는 예외"""
    pass

class BookmarkValidationException(Exception):
    """북마크 데이터 검증 실패 시 발생하는 예외"""
    pass
```

---

## 🎨 **프론트엔드 규칙**

### **1. 파일 구조**
```
src/
├── components/         # 재사용 가능한 컴포넌트
├── pages/             # 페이지 컴포넌트
├── services/          # 비즈니스 로직 서비스
├── stores/            # 상태 관리
├── types/             # TypeScript 타입 정의
├── utils/             # 유틸리티 함수
└── hooks/             # 커스텀 훅
```

### **2. 커스텀 훅 설계**
```typescript
function useBookmarkManagement() {
  /**
   * 북마크 관리를 위한 커스텀 훅
   */
  const createBookmark = useCallback((data: BookmarkCreateData) => {
    // 북마크 생성 로직
  }, [])
  
  const deleteBookmark = useCallback((bookmarkId: number) => {
    // 북마크 삭제 로직
  }, [])
  
  return {
    createBookmark,
    deleteBookmark,
    // 기타 필요한 함수들
  }
}
```

### **3. 상태 관리 패턴**
```typescript
interface BookmarkStoreState {
  bookmarkList: BookmarkNote[]
  currentBookmark: BookmarkNote | null
  isLoadingBookmarks: boolean
  bookmarkCreationError: string | null
}

interface BookmarkStoreActions {
  createNewBookmark: (data: BookmarkCreateData) => Promise<void>
  fetchUserBookmarks: (userId: number) => Promise<void>
  updateBookmarkContent: (id: number, content: string) => Promise<void>
  deleteBookmarkNote: (id: number) => Promise<void>
}
```

---

## 📝 **공통 코딩 스타일**

### **1. 주석 규칙**
```python
# 백엔드 (Python)
def calculate_bookmark_popularity_score(bookmark: Bookmark) -> float:
    """
    북마크의 인기도 점수를 계산합니다.
    
    Args:
        bookmark: 점수를 계산할 북마크 객체
        
    Returns:
        0.0 ~ 100.0 사이의 인기도 점수
        
    Raises:
        BookmarkNotFoundException: 북마크가 존재하지 않는 경우
    """
    # 구현 로직
```

```typescript
// 프론트엔드 (TypeScript)
/**
 * 사용자의 북마크 목록을 페이지네이션과 함께 조회합니다.
 * 
 * @param userId - 조회할 사용자의 ID
 * @param paginationOptions - 페이지네이션 설정
 * @returns 북마크 목록과 페이지네이션 정보를 포함한 응답
 * @throws {BookmarkApiError} API 호출 실패 시
 */
async function fetchUserBookmarkList(
  userId: number, 
  paginationOptions: PaginationOptions
): Promise<BookmarkListResponse> {
  // 구현 로직
}
```

### **2. 에러 메시지**
```python
# 백엔드 - 사용자 친화적 한국어 메시지
raise HTTPException(
    status_code=404, 
    detail="요청하신 북마크를 찾을 수 없습니다. 북마크 ID를 확인해주세요."
)
```

```typescript
// 프론트엔드 - 사용자 친화적 메시지
const createBookmarkErrorMessage = (error: ApiError): string => {
  switch (error.code) {
    case 'BOOKMARK_DUPLICATE':
      return '이미 동일한 URL의 북마크가 존재합니다.'
    case 'BOOKMARK_INVALID_URL':
      return '올바른 URL 형식이 아닙니다. URL을 다시 확인해주세요.'
    default:
      return '북마크 생성 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.'
  }
}
```

---

## 🧪 **테스트 규칙**

### **1. 테스트 클래스 구조**
```python
# 백엔드 테스트
class TestBookmarkManagementService:
    """북마크 관리 서비스 테스트"""
    
    def test_should_create_new_bookmark_when_valid_data_provided(self):
        """유효한 데이터가 제공되었을 때 새로운 북마크를 생성해야 함"""
        # Given (준비)
        # When (실행)
        # Then (검증)
        pass
    
    def test_should_raise_exception_when_duplicate_url_provided(self):
        """중복된 URL이 제공되었을 때 예외를 발생시켜야 함"""
        pass
```

```typescript
// 프론트엔드 테스트
describe('BookmarkApiClient', () => {
  describe('createBookmarkNote', () => {
    it('should create new bookmark when valid data is provided', async () => {
      // Given (준비)
      // When (실행)
      // Then (검증)
    })
    
    it('should throw error when invalid URL is provided', async () => {
      // Given (준비)  
      // When & Then (실행 및 검증)
    })
  })
})
```

### **2. 테스트 데이터 팩토리**
```python
# 백엔드 - Factory Boy 사용
class BookmarkNoteFactory(factory.Factory):
    class Meta:
        model = BookmarkNote
    
    title = factory.Sequence(lambda n: f"테스트 북마크 제목 {n}")
    url = factory.LazyAttribute(lambda obj: f"https://example.com/bookmark-{obj.title}")
    content = factory.Faker('text', max_nb_chars=500)
    created_at = factory.Faker('date_time_this_year')
```

```typescript
// 프론트엔드 - 테스트 헬퍼 함수
function createMockBookmarkNote(overrides?: Partial<BookmarkNote>): BookmarkNote {
  return {
    id: 1,
    title: '테스트 북마크 제목',
    url: 'https://example.com/test-bookmark',
    content: '테스트 북마크 내용입니다.',
    category: 'technology',
    createdAt: new Date(),
    updatedAt: new Date(),
    ...overrides
  }
}
```

---

## ✅ **체크리스트**

### **코드 리뷰 시 확인사항**

#### **명칭 검토**
- [ ] 클래스명이 역할을 명확히 표현하는가?
- [ ] 메서드명이 수행하는 액션을 정확히 설명하는가?
- [ ] 변수명이 저장하는 데이터의 의미를 명확히 전달하는가?
- [ ] 축약어 사용을 최소화했는가?

#### **OOP 원칙 준수**
- [ ] 각 클래스가 단일 책임을 가지는가?
- [ ] 인터페이스와 구현을 분리했는가?
- [ ] 의존성 주입을 적절히 활용했는가?
- [ ] 확장 가능한 구조로 설계했는가?

#### **코드 품질**
- [ ] 한국어 주석으로 의도를 명확히 설명했는가?
- [ ] 에러 메시지가 사용자 친화적인가?
- [ ] 테스트 코드가 충분히 작성되었는가?
- [ ] 타입 안전성을 보장하는가?

---

**이 규칙은 Category Note 프로젝트의 코드 품질과 유지보수성을 향상시키기 위한 가이드라인입니다. 모든 개발자는 이 규칙을 준수하여 일관되고 직관적인 코드를 작성해야 합니다.** 