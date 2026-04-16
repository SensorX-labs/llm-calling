from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.apis.routes import router
from app.core.config import settings

# khởi tạo app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
)

# cấu hình cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# đăng ký route
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    # chạy server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
