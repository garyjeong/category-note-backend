from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.user import User, ProviderType
from app.schemas.user import UserCreate, OAuthUserInfo
from datetime import datetime, timedelta
from jose import jwt
from app.configs.oauth import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_TIME


class AuthController:

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """이메일로 사용자 조회"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_provider(
        db: Session, provider: ProviderType, provider_id: str
    ) -> User:
        """OAuth 제공자와 ID로 사용자 조회"""
        return (
            db.query(User)
            .filter(
                and_(User.provider == provider, User.provider_id == provider_id)
            )
            .first()
        )

    @staticmethod
    def create_user(db: Session, user_data: OAuthUserInfo) -> User:
        """새 사용자 생성"""
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            avatar_url=user_data.avatar_url,
            provider=user_data.provider,
            provider_id=user_data.provider_id,
            is_verified=True,  # OAuth 로그인은 기본적으로 인증된 것으로 처리
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_last_login(db: Session, user: User) -> User:
        """마지막 로그인 시간 업데이트"""
        user.last_login_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def create_access_token(user: User) -> str:
        """JWT 액세스 토큰 생성"""
        payload = {
            "sub": str(user.id),  # JWT 표준에 따라 sub 키 사용
            "user_id": user.id,  # 호환성을 위해 기존 키도 유지
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_TIME),
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> dict:
        """JWT 토큰 검증"""
        try:
            payload = jwt.decode(
                token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None

    @staticmethod
    def get_or_create_user(db: Session, oauth_user: OAuthUserInfo) -> User:
        """OAuth 사용자 정보로 기존 사용자 조회 또는 새 사용자 생성"""
        # 먼저 provider와 provider_id로 조회
        user = AuthController.get_user_by_provider(
            db, oauth_user.provider, oauth_user.provider_id
        )

        if user:
            # 기존 사용자가 있으면 정보 업데이트
            user.full_name = oauth_user.full_name or user.full_name
            user.avatar_url = oauth_user.avatar_url or user.avatar_url
            db.commit()
            db.refresh(user)
            return user

        # 새 사용자 생성
        return AuthController.create_user(db, oauth_user)
