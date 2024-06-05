from fastapi import APIRouter
from api.api_libs.net_lib import get_ip_address

router = APIRouter()

@router.get("/status")
def get_status():
    ip_address = get_ip_address()
    return {"ip": ip_address, "status": "running"}
