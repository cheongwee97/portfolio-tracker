from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class Account:
    account_id: Optional[str]
    username: str
    email: str
    password_hash: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]