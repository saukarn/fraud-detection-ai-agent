import os
import pickle
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

# Load data
df = pd.read_csv("training/kaggle_cc_frd_detection_data.csv")

# Print columns once to confirm
print("CSV Columns:")
print(df.columns.tolist())

# Kaggle Credit Card Fraud dataset columns:
# Time, V1-V28, Amount, Class

features = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

X = df[features]
y = df["Class"]   # Class = 1 fraud, 0 not fraud

# Split data 80/20
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
auc = roc_auc_score(y_test, y_prob)
cm = confusion_matrix(y_test, y_pred)

print("\nMODEL PERFORMANCE")
print("----------------------")
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {auc:.4f}")

print("\nConfusion Matrix:")
print(cm)

# Save model
os.makedirs("models", exist_ok=True)

with open("models/fraud_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nModel saved to models/fraud_model.pkl")