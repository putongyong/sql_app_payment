from pydantic import BaseModel
from datetime import datetime

class PaymentRequest(BaseModel):
    card_number: str
    expiry_month: int
    expiry_year: int
    amount: float
    currency: str
    cvv: int

class PaymentResponse(BaseModel):
    id: int
    card_number: str
    expiry_month: int
    expiry_year: int
    amount: float
    currency: str
    status: str
    cvv: int
    created_at: datetime

    class Config:
        orm_mode = True
