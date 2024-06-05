from fastapi import FastAPI, HTTPException
from api import stock_price, status, lookup

app = FastAPI()

app.include_router(stock_price.router)
app.include_router(status.router)
app.include_router(lookup.router)  # Include the lookup router

@app.get("/")
def read_root():
    return {"message": "Welcome to the Finance API"}