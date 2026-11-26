from dataclasses import dataclass
from typing import Optional

@dataclass
class Item:
    item_id: str                 # Auto-generated, e.g., "EQ-0001" (F1)
    name: str                    # Equipment name (F1, F3)
    category: str                # e.g., "Oscilloscope", "Multimeter", "Hand Tools" (F1, F3)
    manufacturer: str            # Brand / maker (F1)
    model: str                   # Model number/name (F1)
    serial_no: str               # Unique serial number (F1, D1)
    quantity_total: int          # Total units owned (F1)
    quantity_available: int      # Units currently on shelf (F4, F5, F6, F7)
    condition: str               # "Good" | "Damaged" | "Lost" (F1, F7)
    location: str                # Storage shelf/room (F1, F4)
    date_acquired: str           # ISO format "YYYY-MM-DD" (F1)
    image_filename: Optional[str] = None  # "{ItemID}_{random8}.{ext}" in local images/ (F2, Sec 7.3)

@dataclass
class Loan:
    loan_id: str                 # Auto-generated, e.g., "LN-0001" (F5)
    item_id: str                 # Links to Item.item_id (F5)
    borrower_id: str             # Student/Faculty ID number (F5)
    borrower_name: str           # Full name (F5)
    role: str                    # "Student" | "Faculty" (F5, F11)
    purpose: str                 # Lab/class/project reason (F5)
    borrow_date: str             # ISO timestamp "YYYY-MM-DD HH:MM:SS" (F5)
    due_date: str                # ISO format "YYYY-MM-DD" (F5, F8, D6)
    return_date: Optional[str] = None      # Filled on return (F7)
    return_condition: Optional[str] = None # "Good" | "Damaged" | "Lost" (F7)
    status: str = "Active"       # "Active" | "Returned" | "Overdue" (F5, F7, F8)

@dataclass
class WaitlistEntry:
    request_id: str              # Auto-generated, e.g., "WL-0001" (F6)
    item_id: str                 # Equipment requested (F6)
    borrower_id: str             # Student/Faculty ID number (F6)
    borrower_name: str           # Full name (F6)
    role: str                    # "Student" | "Faculty" (F6)
    purpose: str                 # Reason for borrowing (F6)
    requested_at: str            # ISO timestamp for FIFO order (F6, D4)

@dataclass
class UserAccount:
    username: str                # Login ID (F11)
    role: str                    # "Admin" | "Student" | "Faculty" (F11)
    password_hash: str           # PBKDF2 hash — never plain text (F11)
    salt: str                    # Random salt for PBKDF2 (F11)