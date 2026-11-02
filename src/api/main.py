from fastapi import FastAPI

from api.routers import health, rates

app = FastAPI(title="Currency Rates API")

app.include_router(health.router)
app.include_router(rates.router)


@app.get("/")
def root():
    return {"message": "Hello, Lena!"}
