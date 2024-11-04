from app.schemas import schemas
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.crud import crud
from typing import List
from app.db.session import get_db

router = APIRouter()

@router.post("/payments/", response_model=schemas.PaymentResponse)
def create_payment(payment: schemas.PaymentRequest, db: Session = Depends(get_db)):
    db_payment = crud.create_payment(db, payment)
    return db_payment

@router.get("/payments/{payment_id}", response_model=schemas.PaymentResponse)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = crud.get_payment(db, payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    db_payment.card_number = "**** **** **** " + db_payment.card_number[-4:]  # Mask card number
    return db_payment

@router.get("/payments/", response_model=List[schemas.PaymentResponse])
def read_all_payments(
    db: Session = Depends(get_db), 
    offset: int = Query(0, ge=0),  # Default offset to 0
    limit: int = Query(10, gt=0)   # Default limit to 10
):
    payments = crud.get_all_payments(db, offset=offset, limit=limit)
    for payment in payments:
        payment.card_number = "**** **** **** " + payment.card_number[-4:]  # Mask card number
    return payments