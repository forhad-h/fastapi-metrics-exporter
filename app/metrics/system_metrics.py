import time
import gc
import psutil
from prometheus_client import Gauge

PROCESS = psutil.Process()

# Custom Gauges (prefixed with custom_ to avoid collision)
MEM_RESIDENT_BYTES = Gauge(
    "custom_process_resident_memory_bytes", "Resident memory size in bytes"
)
MEM_VIRTUAL_BYTES = Gauge(
    "custom_process_virtual_memory_bytes", "Virtual memory size in bytes"
)

OPEN_FDS = Gauge("custom_process_open_fds", "Number of open file descriptors")
THREAD_COUNT = Gauge("process_thread_count", "Number of threads")
PROCESS_UPTIME_SECONDS = Gauge("process_uptime_seconds", "Process uptime in seconds")

# GC Collections count per generation
GC_COLLECTIONS = Gauge(
    "custom_process_gc_collections_total",
    "Number of times garbage collector has run",
    labelnames=["generation"],
)


def collect_system_metrics():
    MEM_RESIDENT_BYTES.set(PROCESS.memory_info().rss)
    MEM_VIRTUAL_BYTES.set(PROCESS.memory_info().vms)
    OPEN_FDS.set(PROCESS.num_fds())
    THREAD_COUNT.set(PROCESS.num_threads())
    PROCESS_UPTIME_SECONDS.set(time.time() - PROCESS.create_time())

    gc_counts = gc.get_count()
    for gen, count in enumerate(gc_counts):
        GC_COLLECTIONS.labels(generation=str(gen)).set(count)
