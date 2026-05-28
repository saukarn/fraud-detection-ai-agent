def evaluate_rules(txn):
    reasons = []
    score_boost = 0.0

    if txn.amount > txn.customer_avg_amount * 5:
        reasons.append("Transaction amount is much higher than customer average")
        score_boost += 0.25

    if txn.hour < 5:
        reasons.append("Unusual transaction hour")
        score_boost += 0.15

    if txn.transactions_last_24h >= 5:
        reasons.append("High transaction velocity in last 24 hours")
        score_boost += 0.20

    if not txn.card_present and txn.amount > 500:
        reasons.append("High-value card-not-present transaction")
        score_boost += 0.20

    return min(score_boost, 1.0), reasons