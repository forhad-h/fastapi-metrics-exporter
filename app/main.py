from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from app.middleware.metrics_middleware import setup_metrics_middleware
from app.routers import api, health
from app.metrics import system_metrics
from app.config import METRICS_COLLECTION_INTERVAL


# region: Metrics Collection
async def periodic_collection(interval: int = 10):
    while True:
        system_metrics.collect_system_metrics()
        await asyncio.sleep(interval)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background task
    task = asyncio.create_task(periodic_collection(METRICS_COLLECTION_INTERVAL))
    yield
    task.cancel()


# endregion

app = FastAPI(lifespan=lifespan)

# Middlewares
setup_metrics_middleware(app)

# Routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(api.router, prefix="/data", tags=["data"])


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI metrics app!"}
