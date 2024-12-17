from fastapi import FastAPI
from app.api.endpoints import users, currency


app = FastAPI()
app.include_router(users.router, prefix="/auth", tags=["users"])
app.include_router(currency.router, prefix="/currency", tags=["currency"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
