import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "fraud-detection-ai-agent")
    ENV: str = os.getenv("ENV", "local")

    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    DYNAMODB_TABLE: str = os.getenv("DYNAMODB_TABLE", "FraudTransactions")

    ENABLE_DYNAMODB: bool = os.getenv("ENABLE_DYNAMODB", "false").lower() == "true"

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/fraud_model.pkl")

settings = Settings()