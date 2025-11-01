# utils.py
import re
from datetime import datetime
from typing import Optional
from validate_docbr import CPF

cpf_validator = CPF()

def clean_cpf(cpf_str: str) -> str:
    """Remove ., -, / e mantém como string (CPF com 000... é válido)"""
    if not cpf_str or not isinstance(cpf_str, str):
        return ""
    return re.sub(r'\D', '', cpf_str)

def is_valid_cpf(cpf_str: str) -> bool:
    cleaned = clean_cpf(cpf_str)
    return cpf_validator.validate(cleaned) if cleaned else False

def clean_currency(valor: str) -> float:
    """R$ 1.500,75 → 1500.75"""
    if not valor or not isinstance(valor, str):
        return 0.0
    valor = valor.replace('R$', '').replace(' ', '').strip()
    valor = valor.replace('.', '').replace(',', '.')
    try:
        return round(float(valor), 2)
    except (ValueError, TypeError):
        return 0.0

def clean_phone(phone: str) -> str:
    """Remove tudo, mantém só números"""
    if not phone or not isinstance(phone, str):
        return ""
    return re.sub(r'\D', '', phone)

def is_valid_phone(phone: str) -> bool:
    cleaned = clean_phone(phone)
    return len(cleaned) in (10, 11)

def parse_datetime(date_str: str, fmts: list[str]) -> Optional[str]:
    """Tenta converter date_str para ISO (%Y-%m-%d), retorna None se inválido"""
    if not date_str:
        return None
    for fmt in fmts:
        try:
            dt = datetime.strptime(str(date_str).strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None
