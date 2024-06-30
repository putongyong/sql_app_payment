from sqlalchemy.orm import Session
from . import models, schemas, simulate_bank
from datetime import datetime

def create_payment(db: Session, payment: schemas.PaymentRequest):
    db_payment = models.Payment(**payment.model_dump())
    transaction_id, status = simulate_bank.process_payment()
    db_payment.status = status
    db_payment.id=transaction_id
    db_payment.created_at=datetime.now()
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: int):
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()

def get_all_payments(db: Session):
    return db.query(models.Payment).all()
