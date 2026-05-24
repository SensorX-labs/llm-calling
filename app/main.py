import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.apis.routes import router
from app.core.config import settings
from app.consumers.mq_consumer import start_consumer


@asynccontextmanager
async def lifespan(_: FastAPI):
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()
    print(" [info] RabbitMQ Consumer da duoc khoi dong ngam.")
    yield


app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
