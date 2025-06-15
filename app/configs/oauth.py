import os
from authlib.integrations.starlette_client import OAuth

# OAuth 설정
oauth = OAuth()

# 테스트 환경이 아닐 때만 실제 OAuth 설정
if not os.getenv("TESTING"):
    # GitHub OAuth 설정
    oauth.register(
        name="github",
        client_id=os.getenv("GITHUB_CLIENT_ID"),
        client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
        server_metadata_url="https://api.github.com/.well-known/oauth_authorization_server",
        client_kwargs={"scope": "user:email"},
    )

    # Google OAuth 설정
    oauth.register(
        name="google",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid_configuration",
        client_kwargs={"scope": "openid email profile"},
    )
else:
    # 테스트 환경용 더미 OAuth 설정
    oauth.register(
        name="github",
        client_id="test_github_client_id",
        client_secret="test_github_client_secret",
        authorization_endpoint="https://github.com/login/oauth/authorize",
        token_endpoint="https://github.com/login/oauth/access_token",
        client_kwargs={"scope": "user:email"},
    )

    oauth.register(
        name="google",
        client_id="test_google_client_id",
        client_secret="test_google_client_secret",
        authorization_endpoint="https://accounts.google.com/o/oauth2/auth",
        token_endpoint="https://oauth2.googleapis.com/token",
        client_kwargs={"scope": "openid email profile"},
    )

# JWT 설정
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME = 3600  # 1시간
