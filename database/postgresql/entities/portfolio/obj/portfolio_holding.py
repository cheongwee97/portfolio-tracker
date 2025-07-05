from datetime import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass
class PortfolioHolding:
    portfolio_id: str
    portfolio_name: str
    account_id: str
    ticker: str
    quantity: float
    created_at: datetime
    updated_at: datetime