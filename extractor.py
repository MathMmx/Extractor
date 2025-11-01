# extractor.py
import requests
import pandas as pd
import json
import os
from datetime import datetime
from utils import clean_cpf, is_valid_cpf, clean_currency, clean_phone, is_valid_phone, parse_datetime
from pydantic import BaseModel
from jinja2 import Template

class Config(BaseModel):
    api_url: str
    headers: dict
    columns: dict
    output: dict

# Carrega config
with open("config.json") as f:
    config = Config(**json.load(f))

print("Extracting data...")

try:
    response = requests.get(config.api_url, headers=config.headers, timeout=10)
    response.raise_for_status()  # garante HTTP 200
    data = response.json()
except (requests.RequestException, ValueError) as e:
    print(f"Error accessing API: {e}")
    data = []

df = pd.DataFrame(data)
print(f"Received {len(df)} records")

# Apply cleaning and validation
for col, rules in config.columns.items():
    if col not in df.columns:
        continue

    tipo = rules['type']

    if tipo == "cpf":
        df[col] = df[col].apply(clean_cpf)
        df[f'{col}_valid'] = df[col].apply(is_valid_cpf)

    elif tipo == "string_to_int":
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'\D', '', regex=True), errors='coerce').fillna(0).astype(int)

    elif tipo == "email":
        df[f'{col}_valid'] = df[col].astype(str).str.contains('@', na=False)

    elif tipo == "phone":
        df[col] = df[col].apply(clean_phone)
        df[f'{col}_valid'] = df[col].apply(is_valid_phone)

    elif tipo == "currency":
        df[col] = df[col].apply(clean_currency)

    elif tipo == "datetime":
        fmts = rules.get("formats", ["%Y-%m-%d"])
        df[col] = df[col].apply(lambda x: parse_datetime(x, fmts))

# Calculate overdue days if due_date exists
from datetime import datetime

today = datetime.today()

def calculate_days_overdue(due_date_str: str) -> int:
    if not due_date_str:
        return 0  # ou None, se preferir
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    delta = (today - due_date).days
    return delta  # positivo = atrasado, negativo = ainda não venceu

df['days_overdue'] = df['due_date'].apply(calculate_days_overdue)

# Automatic statistics
analysis = {
    "total_records": len(df),
    "valid_cpfs": df['cpf_valid'].sum() if 'cpf_valid' in df.columns else 0,
    "valid_emails": df['email_valid'].sum() if 'email_valid' in df.columns else 0,
    "valid_phones": df['phone_valid'].sum() if 'phone_valid' in df.columns else 0,
    "total_amount": df['valor'].sum() if 'valor' in df.columns else 0,
    "total_overdue_amount": df[df['days_overdue'] > 0]['valor'].sum() if 'valor' in df.columns and 'days_overdue' in df.columns else 0
}

print(f"Valid CPFs: {analysis['valid_cpfs']}/{analysis['total_records']}")
print(f"Total amount: R$ {analysis['total_amount']:,.2f}")
print(f"Total overdue amount: R$ {analysis['total_overdue_amount']:,.2f}")

# Output
os.makedirs("output", exist_ok=True)

if config.output.get('csv'):
    df.to_csv("output/remessa_cleaned.csv", index=False)
    print("CSV generated")

if config.output.get('excel') and len(df) <= 100_000:
    df.to_excel("output/remessa_cleaned.xlsx", index=False)
    print("Excel generated")

if config.output.get('report'):
    template = Template("""
    <h1>Shipment Analysis</h1>
    <p><strong>Total Records:</strong> {{ total_records }}</p>
    <p><strong>Valid CPFs:</strong> {{ valid_cpfs }}</p>
    <p><strong>Total Amount:</strong> R$ {{ "{:,.2f}".format(total_amount) }}</p>
    <p><strong>Total Overdue Amount:</strong> R$ {{ "{:,.2f}".format(total_overdue_amount) }}</p>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            {% for col in df.columns %}
            <th>{{ col }}</th>
            {% endfor %}
        </tr>
        {% for row in df.itertuples(index=False) %}
        <tr>
            {% for value in row %}
            <td>{{ value }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    """)
    html = template.render(
        total_records=analysis['total_records'],
        valid_cpfs=analysis['valid_cpfs'],
        total_amount=analysis['total_amount'],
        total_overdue_amount=analysis['total_overdue_amount'],
        df=df
    )
    with open("output/report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("HTML report generated")
