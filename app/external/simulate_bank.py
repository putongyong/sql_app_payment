import random

def process_payment():
    '''
    ! A simulator of the response coming from a backoffice of a real bank
    We suppose that it will return an id of 6 numbers and a status failure or success
    Without any doubt we can create more complexe id generator or more output types for a better simulation
    '''
    transaction_id = random.randint(100000, 999999)
    status = random.choice(["success", "failure"])
    return transaction_id, status
