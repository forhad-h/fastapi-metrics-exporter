from fastapi import APIRouter, Response
from prometheus_client import generate_latest

router = APIRouter()


@router.get("/")
def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
