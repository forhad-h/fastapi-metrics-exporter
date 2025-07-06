from fastapi import APIRouter
from prometheus_client import Counter
from pydantic import BaseModel


router = APIRouter()

data_post_counter = Counter("data_post_requests_total", "Total POST /data requests")

data_store = []


class DataItem(BaseModel):
    name: str
    value: int


@router.post("/")
async def post_data(item: DataItem):
    data_post_counter.inc()
    data_store.append(item)
    return {"message": "Data Recieved", "data": item}


@router.get("/")
async def get_data():
    return {"data": data_store}
