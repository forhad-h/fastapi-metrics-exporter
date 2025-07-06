# FastAPI Metrics Exporter

## Overview
This project is a FastAPI application that provides comprehensive metrics monitoring capabilities. It exposes application and system metrics in a format compatible with Prometheus scraping.

---

## Metrics Reference Guide

The application exposes the following types of metrics:

### HTTP Metrics
- **Request Count**: Number of HTTP requests received, labeled by method, endpoint, and status code.
- **Request Latency**: Histogram of request processing time in seconds.
- **Request Size**: Size of incoming requests (if implemented).
- **Response Size**: Size of outgoing responses (if implemented).

### System Metrics
- **CPU Usage**: Current CPU usage percentage.
- **Memory Usage**: Current memory usage in bytes and percentage.
- **Disk Usage**: Disk space used and available.
- **Uptime**: Application uptime in seconds.

All metrics are exposed at the `/metrics` endpoint in Prometheus format.

---

## Deployment Instructions (Docker Compose)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd fastapi-metrics-exporter
   ```

2. **Start the application and Prometheus:**
   ```bash
   docker-compose up --build
   ```

3. **Access the services:**
   - FastAPI app: [http://localhost:8000](http://localhost:8000)
   - Metrics endpoint: [http://localhost:8000/metrics](http://localhost:8000/metrics)
   - Prometheus: [http://localhost:9090](http://localhost:9090)

---

## Configuration Options

The following configuration options are available:

- **Prometheus Configuration:**
  - The Prometheus server is configured via `prometheus/prometheus.yml`.
  - You can modify scrape intervals, targets, and other Prometheus settings in this file.

- **Application Settings:**
  - Default FastAPI settings can be adjusted in `app/main.py`.
  - To change the metrics endpoint, update the relevant route in the code.

---

## File Structure

```
app/
  main.py                # FastAPI app entry point
  metrics/               # Metrics collection modules
  middleware/            # Middleware for metrics
  routers/               # API and health endpoints
prometheus/
  prometheus.yml         # Prometheus configuration
docker-compose.yml       # Multi-service orchestration
Dockerfile               # App container definition
requirements.txt         # Python dependencies
```

---

## License
MIT License
