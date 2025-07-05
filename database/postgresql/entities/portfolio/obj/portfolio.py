
from typing import Optional
from dataclasses import dataclass

@dataclass
class Porfolio:
    portfolio_id: Optional[str]
    portfolio_name: str
    account_id: str
