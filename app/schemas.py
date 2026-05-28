from pydantic import BaseModel
from typing import List

class TransactionRequest(BaseModel):
    transaction_id: str
    customer_id: str
    amount: float
    merchant_category: str
    country: str
    card_present: bool
    hour: int
    customer_avg_amount: float
    transactions_last_24h: int

class FraudResponse(BaseModel):
    transaction_id: str
    fraud_score: float
    risk_level: str
    decision: str
    reasons: List[str]
    llm_explanation: str