from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import lifespan
from app.routes.auth import router as auth_router
from app.routes.task import router as task_router

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(task_router)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "Python FastAPI for the back-end API.",
        "health": "/health"
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
