import os

from dotenv import load_dotenv

from app.models import get_model


load_dotenv()


provider = os.getenv("MODEL_PROVIDER", "mock")

model = get_model(provider)

response = model.generate(
    "Explain what a brute-force attack is in simple terms."
)

print(response)
