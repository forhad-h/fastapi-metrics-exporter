from fastapi import FastAPI
from app.middleware.metrics_middleware import setup_metrics_middleware
from app.routers import api, health

app = FastAPI()

# Middlewares
setup_metrics_middleware(app)

# Routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(api.router, prefix="/data", tags=["data"])


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI metrics app!"}
