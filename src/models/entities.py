from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Item:
    item_id: str
    name: str
    category: str
    quantity_total: int
    quantity_available: int
    location: str = ""
    condition: str = "Good"
    image_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Loan:
    loan_id: str
    item_id: str
    borrower_name: str
    borrower_contact: str
    quantity: int
    borrowed_at: str
    due_at: str
    returned_at: Optional[str] = None
    status: str = "active"  # e.g., "active", "returned", "overdue"


@dataclass
class WaitlistEntry:
    entry_id: str
    item_id: str
    requester_name: str
    requester_contact: str
    priority: int = 1
    requested_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "waiting"  # e.g., "waiting", "notified", "fulfilled", "cancelled"


@dataclass
class UserAccount:
    user_id: str
    username: str
    password_hash: str
    salt: str
    role: str = "staff"  # e.g., "admin", "staff", "viewer"
    is_active: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())