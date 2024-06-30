from pydantic import BaseModel
from datetime import datetime

class PaymentRequest(BaseModel):
    '''
    ! This is a model extending the pydantic base model
    Its purpose is to create the input data type for payment request
    '''
    card_number: str
    expiry_month: int
    expiry_year: int
    amount: float
    currency: str
    cvv: int

class PaymentResponse(BaseModel):
    '''
    ! This is a model extending the pydantic base model
    Its purpose is to create the output data type for payment response
    '''
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
