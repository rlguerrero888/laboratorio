import pandas as pd

from data_ai.fintech.models import SUPPORTED_CURRENCIES


def check_invalid_amount(df: pd.DataFrame) -> pd.Series:
    """Returns True for rows where amount <= 0."""
    return df["amount"].le(0)


def check_unsupported_currency(df: pd.DataFrame) -> pd.Series:
    """Returns True for rows whose currency is not in SUPPORTED_CURRENCIES."""
    currency = df["currency"].fillna("").astype(str).str.upper()
    return ~currency.isin(SUPPORTED_CURRENCIES)


def check_missing_merchant(df: pd.DataFrame) -> pd.Series:
    """Returns True for rows with a null merchant_id."""
    return df["merchant_id"].isna()
