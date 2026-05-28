import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0
)

def generate_explanation(txn, score, risk_level, reasons):
    prompt = f"""
You are a fraud risk analyst.

Explain why this transaction received this risk rating.

Transaction:
- Amount: {txn.amount}
- Merchant category: {txn.merchant_category}
- Country: {txn.country}
- Card present: {txn.card_present}
- Hour: {txn.hour}
- Customer average amount: {txn.customer_avg_amount}
- Transactions last 24h: {txn.transactions_last_24h}

Fraud score: {score}
Risk level: {risk_level}
Reasons: {reasons}

Return a concise business-friendly explanation.
"""
    response = llm.invoke(prompt)
    return response.content