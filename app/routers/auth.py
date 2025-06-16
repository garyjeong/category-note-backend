from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.configs.oauth import oauth, JWT_EXPIRATION_TIME
from app.controllers.auth_controller import AuthController
from app.schemas.user import TokenResponse, OAuthUserInfo
from app.models.user import User, ProviderType
import httpx

router = APIRouter()


@router.get("/signin/{provider}")
async def signin(provider: ProviderType, request: Request):
    """OAuth 로그인 시작"""

    # OAuth 제공자별 리다이렉트 URL 설정
    redirect_uri = str(request.url_for("auth_callback", provider=provider))

    # OAuth 인증 URL로 리다이렉트
    return await oauth.create_client(provider.value).authorize_redirect(
        request, redirect_uri
    )


@router.get("/callback/{provider}")
async def auth_callback(
    provider: ProviderType, request: Request, db: Session = Depends(get_db)
):
    """OAuth 콜백 처리"""

    try:
        # OAuth 토큰 받기
        client = oauth.create_client(provider.value)
        token = await client.authorize_access_token(request)

        # 사용자 정보 가져오기
        if provider == ProviderType.GITHUB:
            user_info = await _get_github_user_info(token)
        elif provider == ProviderType.GOOGLE:
            user_info = await _get_google_user_info(token)

        # 사용자 생성 또는 조회
        user = AuthController.get_or_create_user(db, user_info)

        # 마지막 로그인 시간 업데이트
        user = AuthController.update_last_login(db, user)

        # JWT 토큰 생성
        access_token = AuthController.create_access_token(user)

        # 클라이언트로 리다이렉트 (프론트엔드 URL)
        frontend_url = (
            f"http://localhost:3000/auth/success?token={access_token}"
        )
        return RedirectResponse(url=frontend_url)

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"OAuth 인증 실패: {str(e)}"
        )


async def _get_github_user_info(token: dict) -> OAuthUserInfo:
    """GitHub 사용자 정보 조회"""
    async with httpx.AsyncClient() as client:
        # 사용자 기본 정보
        response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {token['access_token']}"},
        )
        user_data = response.json()

        # 이메일 정보 (private일 수 있음)
        email_response = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"Bearer {token['access_token']}"},
        )
        emails = email_response.json()
        primary_email = next(
            (email["email"] for email in emails if email["primary"]),
            user_data.get("email"),
        )

        return OAuthUserInfo(
            email=primary_email,
            username=user_data["login"],
            full_name=user_data.get("name"),
            avatar_url=user_data.get("avatar_url"),
            provider=ProviderType.GITHUB,
            provider_id=str(user_data["id"]),
        )


async def _get_google_user_info(token: dict) -> OAuthUserInfo:
    """Google 사용자 정보 조회"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token['access_token']}"},
        )
        user_data = response.json()

        return OAuthUserInfo(
            email=user_data["email"],
            username=user_data.get(
                "given_name", user_data["email"].split("@")[0]
            ),
            full_name=user_data.get("name"),
            avatar_url=user_data.get("picture"),
            provider=ProviderType.GOOGLE,
            provider_id=user_data["id"],
        )


@router.post("/logout")
async def logout():
    """로그아웃 (클라이언트에서 토큰 삭제)"""
    return {"message": "로그아웃 되었습니다."}
