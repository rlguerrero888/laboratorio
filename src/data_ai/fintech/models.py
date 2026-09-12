from dataclasses import dataclass

SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "CAD", "MXN"]


@dataclass
class ValidationReport:
    total_transactions: int
    invalid_amount: int
    unsupported_currency: int
    missing_merchant: int
    valid_transactions: int
