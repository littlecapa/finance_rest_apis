from fastapi import APIRouter
#from api.provider.financialmodelingprep import financeModeling

#fm = financeModeling()

router = APIRouter()

#@router.get("/stock_price/{symbol}")
#async def get_stock_price(symbol: str):
#    return fm.get_stock_price(symbol)

#
# New API for ISIN. Will serve as a template
#

@router.get("/stock_price_isin/{isin}")
async def get_stock_price_isin(isin: str):
    return {'price': 0.0, 'currency': 'xxx'}
