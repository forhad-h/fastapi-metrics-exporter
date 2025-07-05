from fastapi import APIRouter
from prometheus_client import Counter

router = APIRouter()

data_post_counter = Counter("data_post_requests_total", "Total POST /data requests")

data_store = []


@router.post("/")
async def post_data(item: DataItem):
    data_post_counter.inc()
    data_store.append(item)
    return {"message": "Data Recieved", "data": item}


@router.get("/")
async def get_data():
    return {"data": data_store}
