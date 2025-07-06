from fastapi import APIRouter
import math
import time

router = APIRouter()


@router.get("/stress-cpu")
def stress_cpu(seconds: int = 3):
    # Simulate high CPU usage for N seconds
    start = time.time()
    while time.time() - start < seconds:
        # Do some meaningless math to keep CPU busy
        for _ in range(10000):
            math.sqrt(12345.6789)
    return {"status": "done", "duration": seconds}


@router.get("/stress-memory")
def stress_memory(seconds: int = 3, megabytes: int = 100):
    """
    Simulate high memory usage by allocating ~`megabytes` MB for `seconds` seconds.
    """
    block_size = 1024 * 1024  # 1MB
    blocks = []

    try:
        for _ in range(megabytes):
            blocks.append(bytearray(block_size))  # allocate 1MB blocks

        time.sleep(seconds)  # hold the memory for some time
    except MemoryError:
        return {"status": "failed", "error": "MemoryError during allocation"}

    return {"status": "done", "duration": seconds, "memory_allocated_mb": megabytes}
