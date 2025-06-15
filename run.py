#!/usr/bin/env python3
"""
Category Note Backend 서버 실행 스크립트
"""

import uvicorn
import os

if __name__ == "__main__":
    # 환경변수에서 호스트와 포트 읽기 (기본값 설정)
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    # 개발 환경에서는 reload=True로 설정
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,  # 개발 환경
        log_level="info",
    )
