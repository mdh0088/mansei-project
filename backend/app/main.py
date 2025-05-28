from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.v1 import auth, mansei
from app.core.config import settings

app = FastAPI(
    title="만세력 계산 서비스",
    description="한국 전통 명리학 기반 만세력 계산 API",
    version="1.0.0"
)

# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(mansei.router, prefix="/api/v1/mansei", tags=["mansei"])

@app.get("/")
async def root():
    return {"message": "만세력 계산 서비스 API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 글로벌 예외 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )
