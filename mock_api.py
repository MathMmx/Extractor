# mock_api.py
from fastapi import FastAPI
from validate_docbr import CPF
import random
from datetime import datetime, timedelta

app = FastAPI()

cpf_generator = CPF()

def generate_valid_cpf() -> str:
    """Generates a random valid CPF"""
    return cpf_generator.generate()

def generate_due_date(max_future_days: int = 30) -> str:
    """Generates a random future date within the next max_future_days days (YYYY-MM-DD)"""
    days = random.randint(1, max_future_days)
    future_date = datetime.now() + timedelta(days=days)
    return future_date.strftime("%Y-%m-%d")

def generate_item() -> dict:
    """Generates a random client/remittance item"""
    return {
        "id": random.randint(1, 9999),
        "name": f"Client {random.randint(1, 100)}",
        "cpf": generate_valid_cpf(),
        "phone": f"(21) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}",
        "amount": round(random.uniform(10, 1000), 2),
        "due_date": generate_due_date()
    }

@app.get("/remessa")
def get_remessa() -> list[dict]:
    """Returns a list of random items"""
    return [generate_item() for _ in range(random.randint(5, 15))]

if __name__ == "__main__":
    import uvicorn
    print("API running at http://localhost:8000/remessa")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
