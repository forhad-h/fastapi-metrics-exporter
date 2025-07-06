from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from app.middleware.metrics_middleware import MetricsMiddleware
from app.routers import api, health
from app.metrics import system_metrics
from app.metrics.routes import router as metrics_router
from app.config import METRICS_COLLECTION_INTERVAL
import debugpy

debugpy.listen(("0.0.0.0", 5678))
print("⚡ Waiting for debugger attach...")


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
app.add_middleware(MetricsMiddleware)

# Routers
app.include_router(metrics_router, prefix="/metrics", tags=["metrics"])
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(api.router, prefix="/data", tags=["data"])


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI metrics app!"}
