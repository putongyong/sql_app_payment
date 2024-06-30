import random

def process_payment():
    transaction_id = random.randint(100000, 999999)
    status = random.choice(["success", "failure"])
    return transaction_id, status
