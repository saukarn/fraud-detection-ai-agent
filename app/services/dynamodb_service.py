import os
import boto3
from datetime import datetime, timezone
from decimal import Decimal
from app.config import settings

#dynamodb = boto3.resource("dynamodb")
#table = dynamodb.Table(os.getenv("DYNAMODB_TABLE", "FraudTransactions"))
dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION)

table = dynamodb.Table(settings.DYNAMODB_TABLE)

def save_transaction_result(state):
    if not settings.ENABLE_DYNAMODB:
        print("Skipping DynamoDB save because ENABLE_DYNAMODB=false")
        return
    txn = state["txn"]

    item = {
        "transaction_id": txn.transaction_id,
        "customer_id": txn.customer_id,
        "amount": Decimal(str(txn.amount)),
        "fraud_score": Decimal(str(state["final_score"])),
        "risk_level": state["risk_level"],
        "decision": state["decision"],
        "reasons": state["reasons"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    table.put_item(Item=item)