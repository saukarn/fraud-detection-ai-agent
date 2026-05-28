import pickle
import pandas as pd

with open("models/fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_fraud_score(txn):
    row = pd.DataFrame([{
        "amount": txn.amount,
        "hour": txn.hour,
        "customer_avg_amount": txn.customer_avg_amount,
        "transactions_last_24h": txn.transactions_last_24h,
        "card_present": int(txn.card_present)
    }])

    probability = model.predict_proba(row)[0][1]
    return float(probability)