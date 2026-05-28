from fastapi import FastAPI
from app.schemas import TransactionRequest, FraudResponse
from app.agent.fraud_graph import run_fraud_agent

app = FastAPI(title="Fraud Detection AI Agent")

@app.get("/health")
def health():
    return {"status": "UP"}

@app.post("/transactions/score", response_model=FraudResponse)
def score_transaction(request: TransactionRequest):
    return run_fraud_agent(request)