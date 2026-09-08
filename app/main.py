from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .config import settings
from .seed import seed
from .mqtt import start_mqtt
from .routers import auth, tracking, gps

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed()
    start_mqtt()
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tracking.router, prefix="/api", tags=["Tracking"])
app.include_router(gps.router, prefix="/api/gps", tags=["GPS"])

@app.get("/health")
def health():
    return {"status": "ok"}
