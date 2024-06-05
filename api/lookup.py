from fastapi import APIRouter
from api.provider.open_figi import openFigi

provider = openFigi()

router = APIRouter()

@router.get("/lookup/isin/{isin}")
async def get_stock_by_isin(isin: str):
    return provider.isin2symbol(isin)

@router.get("/lookup/wkn/{wkn}")
async def get_stock_by_wkn(wkn: str):
    return provider.wkn2symbol(wkn)