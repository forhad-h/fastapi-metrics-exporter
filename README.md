# FastAPI Metrics Monitoring System

## Overview

This project is a production-ready FastAPI application that provides comprehensive system-level and application-level metrics monitoring. It exposes detailed performance metrics in Prometheus format, enabling real-time observability of both infrastructure health and application behavior. The stack includes Prometheus for metrics storage and querying, and Grafana for advanced dashboard visualization.

---

## Quick Start: Running the Stack and Visualizing Metrics

> **Notice:**
>
> This project requires:
> - **Docker:** 20.10.0 or newer (tested with 28.3.1)
> - **Docker Compose:** V2 plugin (use `docker compose` command), 2.0.0 or newer (tested with v2.38.1)
>   - Compose V2 is included with Docker Engine 20.10+ and is recommended over the legacy `docker-compose` command.


### 1. Clone and Start the Project

```bash
git clone https://github.com/forhad-h/fastapi-metrics-exporter
cd fastapi-metrics-exporter
docker compose up --build
```

This will start the FastAPI app, Prometheus, and Grafana.

### 2. Access the Services

- **FastAPI app:** [http://localhost:8000](http://localhost:8000)
- **Metrics endpoint:** [http://localhost:8000/metrics](http://localhost:8000/metrics)
- **Prometheus:** [http://localhost:9090](http://localhost:9090)
- **Grafana:** [http://localhost:3000](http://localhost:3000) (default login: `admin` / `admin`)

### 3. Import the Grafana Dashboard

1. Log in to Grafana at [http://localhost:3000](http://localhost:3000).
2. Add Prometheus as a data source (URL: `http://prometheus:9090`).
3. Go to **Dashboards → Import**, upload `monitoring/dashboards/fastapi-metrics.json`.
4. The dashboard will visualize FastAPI and system metrics in real time.

#### Connecting Grafana to Prometheus
- In Grafana, navigate to **Configuration → Data Sources → Add data source → Prometheus**.
- Set the URL to `http://prometheus:9090` and save.

---

## API Endpoints and Stress Test Utilities

The application provides several endpoints for monitoring and testing:

- `GET /` — Root endpoint
- `GET /health` — Health check
- `GET /metrics` — Prometheus metrics exposition
- `POST /data` — Sample data processing
- `GET /data` — Sample data retrieval
- `GET /stress/cpu` — **CPU stress test** (simulates CPU load)
- `GET /stress/memory` — **Memory stress test** (simulates memory usage)

You can use the `/stress/cpu` and `/stress/memory` endpoints to generate artificial load and observe the effect on system metrics in real time via Grafana or Prometheus.

---

## Why Use `prometheus_client` Instead of `prometheus_fastapi_instrumentator`?

This project uses the low-level [`prometheus_client`](https://github.com/prometheus/client_python) library to implement metrics collection and exposition. This approach is chosen to provide a deeper understanding of Prometheus metrics, custom metric creation, and manual instrumentation. 

**Note:** For production deployments where rapid setup and best practices are desired, [`prometheus_fastapi_instrumentator`](https://github.com/trallard/prometheus-fastapi-instrumentator) is recommended. It offers automatic instrumentation and is easier to integrate, but using `prometheus_client` directly is valuable for learning and for advanced customization.

---

## Metrics Reference Guide

### HTTP Metrics
- **http_requests_total**: Counter for total HTTP requests, labeled by method, endpoint, and status code.
- **http_request_duration_seconds**: Histogram of request processing time in seconds.
- **Request/Response Size**: Histograms for request and response sizes (if implemented).

### System Metrics
- **process_cpu_seconds_total**: Total CPU time consumed by the process.
- **CPU Usage Rate**: `rate(process_cpu_seconds_total[5m])` for CPU usage trends.
- **process_resident_memory_bytes**: Physical memory used.
- **process_virtual_memory_bytes**: Virtual memory allocated.
- **Uptime**: Application uptime in seconds.
- **File Descriptor Usage, GC Stats, Thread Count**: Additional process-level metrics.

All metrics are exposed at `/metrics` in Prometheus format.

---

## Configuration Options

- **Prometheus:**
  - Configured via `prometheus/prometheus.yml` (edit scrape intervals, targets, etc.).
- **Grafana:**
  - Import dashboards from `monitoring/dashboards/fastapi-metrics.json`.
- **Application:**
  - Main settings in `app/main.py` and `app/config.py`.
  - To change the metrics endpoint, update the relevant route in the code.
  - Metric collection intervals and histogram buckets can be customized in the metrics modules.

---

## File Structure

```
app/
  main.py                # FastAPI app entry point
  config.py              # App configuration
  metrics/               # Metrics collection modules
    system_metrics.py    # System metrics (CPU, memory, etc.)
    http_metrics.py      # HTTP request metrics
    routes.py            # Metrics routes
  middleware/            # Middleware for metrics
    metrics_middleware.py
  routers/               # API and health endpoints
    api.py
    health.py
    test.py
prometheus/
  prometheus.yml         # Prometheus configuration
monitoring/
  dashboards/
    fastapi-metrics.json # Grafana dashboard
docker-compose.yml       # Multi-service orchestration
Dockerfile               # App container definition
requirements.txt         # Python dependencies
```

---

## License
MIT License
