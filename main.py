from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
import asyncio
import uvicorn
import models.crud as crud
import models.schemas as schemas
import models.models as models
from database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def get_home():
    return {"message": "Welcome to the payment API"}

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

@app.get("/payments/", response_model=List[schemas.PaymentResponse])
def read_all_payments(
    db: Session = Depends(get_db), 
    offset: int = Query(0, ge=0),  # Default offset to 0
    limit: int = Query(10, gt=0)   # Default limit to 10
):
    payments = crud.get_all_payments(db, offset=offset, limit=limit)
    for payment in payments:
        payment.card_number = "**** **** **** " + payment.card_number[-4:]  # Mask card number
    return payments

async def main():
    config = uvicorn.Config("main:app", host='0.0.0.0', port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())