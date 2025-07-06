import psutil
import gc
from prometheus_client import Gauge, REGISTRY


def get_or_create_gauge(name, documentation, labelnames=()):
    try:
        metric = REGISTRY._names_to_collectors.get(name)

        if metric:
            return metric
    except Exception:
        pass
    return Gauge(name, documentation, labelnames)


PROCESS = psutil.Process()

# CPU Metrics
CPU_SECONDS_TOTAL = get_or_create_gauge(
    "process_cpu_seconds_total", "Total CPU seconds used by the process"
)
CPU_USAGE_PERCENT = get_or_create_gauge(
    "process_cpu_percent", "Process CPU utilization percentage"
)

# Memory Metrics
MEM_RESIDENT_BYTES = get_or_create_gauge(
    "process_resident_memory_bytes", "Resident memory size in bytes"
)
MEM_VIRTUAL_BYTES = get_or_create_gauge(
    "process_virtual_memory_bytes", "Virtual memory size in bytes"
)

# File Descriptors Metrics
FILE_DESCRIPTORS = get_or_create_gauge(
    "process_open_fds", "Number of open file descriptors"
)

# Threads Metrics
THREAD_COUNT = get_or_create_gauge("process_thread_count", "Number of threads")

# Process Metrics
PROCESS_START_TIME = get_or_create_gauge(
    "process_start_time_seconds",
    "Start time of the processs since unix epoch in seconds",
)
PROCESS_UPTIME = get_or_create_gauge(
    "process_uptime_seconds", "Process uptime in seconds"
)

# Garbage Collection Metrics
GC_COLLECTED = get_or_create_gauge(
    "process_gc_collections_total",
    "Number of times garbage collector has run",
    labelnames=["generation"],
)


def collect_system_metrics():
    CPU_SECONDS_TOTAL.set(PROCESS.cpu_times().user + PROCESS.cpu_times().system)
    CPU_USAGE_PERCENT.set(PROCESS.cpu_percent(interval=0.1))

    MEM_RESIDENT_BYTES.set(PROCESS.memory_info().rss)
    MEM_VIRTUAL_BYTES.set(PROCESS.memory_info().vms)

    FILE_DESCRIPTORS.set(PROCESS.num_fds())

    THREAD_COUNT.set(PROCESS.num_threads())

    PROCESS_START_TIME.set(PROCESS.create_time())
    PROCESS_UPTIME.set(PROCESS.time() - PROCESS.create_time())

    gc_stats = gc.get_count()
    for i, count in enumerate(gc_stats):
        GC_COLLECTED.labels(generation=str(i)).set(count)
