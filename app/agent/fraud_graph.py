from typing import TypedDict, List
from langgraph.graph import StateGraph, END

from app.services.fraud_rules import evaluate_rules
from app.services.ml_model import predict_fraud_score
from app.services.llm_service import generate_explanation
from app.services.dynamodb_service import save_transaction_result

class FraudState(TypedDict):
    txn: object
    rule_score: float
    ml_score: float
    final_score: float
    reasons: List[str]
    risk_level: str
    decision: str
    explanation: str

def run_rules_node(state: FraudState):
    score, reasons = evaluate_rules(state["txn"])
    return {"rule_score": score, "reasons": reasons}

def run_ml_node(state: FraudState):
    ml_score = predict_fraud_score(state["txn"])
    return {"ml_score": ml_score}

def combine_scores_node(state: FraudState):
    final_score = round((state["ml_score"] * 0.7) + (state["rule_score"] * 0.3), 2)

    if final_score >= 0.75:
        risk_level = "HIGH"
        decision = "REVIEW"
    elif final_score >= 0.40:
        risk_level = "MEDIUM"
        decision = "MONITOR"
    else:
        risk_level = "LOW"
        decision = "APPROVE"

    return {
        "final_score": final_score,
        "risk_level": risk_level,
        "decision": decision
    }

def explain_node(state: FraudState):
    explanation = generate_explanation(
        txn=state["txn"],
        score=state["final_score"],
        risk_level=state["risk_level"],
        reasons=state["reasons"]
    )
    return {"explanation": explanation}

def save_node(state: FraudState):
    save_transaction_result(state)
    return {}

workflow = StateGraph(FraudState)

workflow.add_node("rules", run_rules_node)
workflow.add_node("ml", run_ml_node)
workflow.add_node("combine", combine_scores_node)
workflow.add_node("explain", explain_node)
workflow.add_node("save", save_node)

workflow.set_entry_point("rules")
workflow.add_edge("rules", "ml")
workflow.add_edge("ml", "combine")
workflow.add_edge("combine", "explain")
workflow.add_edge("explain", "save")
workflow.add_edge("save", END)

graph = workflow.compile()

def run_fraud_agent(txn):
    result = graph.invoke({"txn": txn})

    return {
        "transaction_id": txn.transaction_id,
        "fraud_score": result["final_score"],
        "risk_level": result["risk_level"],
        "decision": result["decision"],
        "reasons": result["reasons"],
        "llm_explanation": result["explanation"]
    }