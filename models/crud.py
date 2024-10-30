from sqlalchemy.orm import Session
from . import models, schemas, simulate_bank
from datetime import datetime

def create_payment(db: Session, payment: schemas.PaymentRequest):
    # get the input data and turning it into a dictionary
    db_payment = models.Payment(**payment.model_dump())
    # get the transaction id and the status from the simulator
    # in the future this will be replace by a real request to a backoffice of a bank
    transaction_id, status = simulate_bank.process_payment()
    # add the status to the input
    db_payment.status = status
    # add the transaction id
    db_payment.id=transaction_id
    # get the current time
    # in real life cases, this time maybe provided by the bank to track the history
    db_payment.created_at=datetime.now()
    # insert the data into the database table
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: int):
    # get the data by payment id
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()

def get_all_payments(db: Session, offset: int = 0, limit: int = 10):
    # Fetch payments with pagination
    return db.query(models.Payment).offset(offset).limit(limit).all()
