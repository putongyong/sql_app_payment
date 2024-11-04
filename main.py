from app.api.controllers import items
from fastapi import FastAPI
import asyncio
import uvicorn
from app.models import models
from app.db.session import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)

@app.get("/")
def get_home():
    return {"message": "Welcome to the payment API"}

async def main():
    config = uvicorn.Config("main:app", host='0.0.0.0', port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())