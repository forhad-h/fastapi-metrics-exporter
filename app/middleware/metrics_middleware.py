import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import generate_latest
from app.metrics.http_metrics import record_request


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        method = request.method
        endpoint = request.url.path
        status_code = response.status_code

        endpoint = request.url.path
        method = request.method

        record_request(method, endpoint, status_code, process_time)

        return response
