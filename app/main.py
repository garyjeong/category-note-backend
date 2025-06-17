from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.configs.database import engine
from app.models import user, url, bookmark
from app.routers import auth, url as url_router, bookmark as bookmark_router
import os

# 테스트 환경이 아닐 때만 데이터베이스 테이블 생성
if not os.getenv("TESTING"):
    user.Base.metadata.create_all(bind=engine)
    url.Base.metadata.create_all(bind=engine)
    bookmark.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Category Note API",
    description="YouTube와 지식 웹 페이지를 정리하는 API",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(url_router.router, prefix="/api", tags=["urls"])
app.include_router(bookmark_router.router, tags=["bookmark"])


@app.get("/")
async def root():
    return {"message": "Category Note API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
