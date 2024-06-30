from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import asyncio
import uvicorn
from datetime import datetime
import models.crud as crud
import models.schemas as schemas
import models.simulate_bank as simulate_bank
import models.models as models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/payments/", response_model=schemas.PaymentResponse)
def create_payment(payment: schemas.PaymentRequest, db: Session = Depends(get_db)):
    db_payment = crud.create_payment(db, payment)
    return db_payment

@app.get("/payments/{payment_id}", response_model=schemas.PaymentResponse)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = crud.get_payment(db, payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    db_payment.card_number = "**** **** **** " + db_payment.card_number[-4:]  # Mask card number
    return db_payment

async def main():
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())