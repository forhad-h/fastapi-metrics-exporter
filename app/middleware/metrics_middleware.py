from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from promethues_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Request Latency", ["endpoint"]
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        endpoint = request.url.path
        method = request.method
        with REQUEST_LATENCY.labels(endpoint=endpoint).time():
            response = await call_next(request)
        REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
        return response


def setup_metrics_middleware(app):
    app.add_middleware(MetricsMiddleware)

    @app.get("/metrics")
    async def metrics():
        return Response(contenct=generate_latest(), media_type="text/plain")
