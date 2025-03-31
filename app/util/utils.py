# utils.py
from datetime import datetime

def get_today(date_format: str = '%Y-%m-%d') -> str:
    return datetime.now().strftime(date_format)
