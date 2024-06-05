from fastapi import APIRouter
from api.provider.financialmodelingprep import financeModeling

fm = financeModeling()

router = APIRouter()

@router.get("/stock_price/{symbol}")
async def get_stock_price(symbol: str):
    return fm.get_stock_price(symbol)