import pandas as pd

from data_ai.fintech.dq.rules import (
    check_invalid_amount,
    check_missing_merchant,
    check_unsupported_currency,
)
from data_ai.fintech.models import ValidationReport


class TransactionValidationEngine:
    def validate(self, transactions_df: pd.DataFrame) -> ValidationReport:
        """
        Applies the three rules from rules.py and returns a ValidationReport.
        valid_transactions = rows that fail NONE of the rules.
        """
        total_transactions = len(transactions_df)

        invalid_amount_mask = check_invalid_amount(transactions_df)
        unsupported_currency_mask = check_unsupported_currency(transactions_df)
        missing_merchant_mask = check_missing_merchant(transactions_df)

        invalid_amount = int(invalid_amount_mask.sum())
        unsupported_currency = int(unsupported_currency_mask.sum())
        missing_merchant = int(missing_merchant_mask.sum())

        valid_mask = ~(
            invalid_amount_mask
            | unsupported_currency_mask
            | missing_merchant_mask
        )
        valid_transactions = int(valid_mask.sum())

        return ValidationReport(
            total_transactions=total_transactions,
            invalid_amount=invalid_amount,
            unsupported_currency=unsupported_currency,
            missing_merchant=missing_merchant,
            valid_transactions=valid_transactions,
        )
