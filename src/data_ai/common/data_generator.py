from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def generate_fintech_data(seed: int = 42) -> dict[str, pd.DataFrame]:
    """Generate synthetic fintech datasets with ~5% dirty rows, matching the senior consultant notebook."""
    np.random.seed(seed)

    n_accounts = 300
    accounts = pd.DataFrame(
        {
            "account_id": [f"A{i:04d}" for i in range(1, n_accounts + 1)],
            "customer_id": [f"CU{i:04d}" for i in range(1, n_accounts + 1)],
            "account_type": np.random.choice(
                ["checking", "savings", "credit", "prepaid"],
                n_accounts,
                p=[0.35, 0.30, 0.25, 0.10],
            ),
            "state": np.random.choice(
                ["CA", "TX", "NY", "FL", "IL", "WA", "GA"], n_accounts
            ),
            "opened_date": [
                datetime(2020, 1, 1) + timedelta(days=int(d))
                for d in np.random.randint(0, 1460, n_accounts)
            ],
        }
    )

    n_merchants = 30
    merchants = pd.DataFrame(
        {
            "merchant_id": [f"M{i:03d}" for i in range(1, n_merchants + 1)],
            "name": [f"Merchant_{i}" for i in range(1, n_merchants + 1)],
            "category": np.random.choice(
                ["Food & Beverage", "Travel", "Retail", "Entertainment", "Utilities"],
                n_merchants,
            ),
            "country": np.random.choice(["US", "GB", "CA", "MX", "FR"], n_merchants),
        }
    )

    n_transactions = 1000
    base_date = datetime(2024, 1, 1)
    txn_dates = [
        base_date + timedelta(days=int(d))
        for d in np.random.randint(0, 365, n_transactions)
    ]

    transactions = pd.DataFrame(
        {
            "transaction_id": [f"T{i:06d}" for i in range(1, n_transactions + 1)],
            "account_id": np.random.choice(accounts["account_id"], n_transactions),
            "merchant_id": np.random.choice(
                merchants["merchant_id"], n_transactions
            ),
            "transaction_date": txn_dates,
            "amount": np.round(np.random.uniform(1, 500, n_transactions), 2),
            "currency": np.random.choice(
                ["USD", "EUR", "GBP", "CAD", "MXN"],
                n_transactions,
                p=[0.70, 0.10, 0.10, 0.05, 0.05],
            ),
            "transaction_type": np.random.choice(
                ["purchase", "refund", "transfer", "withdrawal"],
                n_transactions,
                p=[0.70, 0.10, 0.10, 0.10],
            ),
            "status": np.random.choice(
                ["approved", "declined", "pending", "flagged"],
                n_transactions,
                p=[0.75, 0.10, 0.10, 0.05],
            ),
        }
    )

    # Inject dirty rows (~5%)
    dirty_idx = np.random.choice(n_transactions, 50, replace=False)
    transactions.loc[dirty_idx[:10], "amount"] = -50.00
    transactions.loc[dirty_idx[10:20], "merchant_id"] = None
    transactions.loc[dirty_idx[20:30], "currency"] = "XYZ"
    transactions.loc[dirty_idx[30:40], "transaction_date"] = datetime(2026, 12, 1)
    transactions.loc[dirty_idx[40:50], "transaction_id"] = transactions.loc[
        dirty_idx[:10], "transaction_id"
    ].values

    n_limits = 300
    limits = pd.DataFrame(
        {
            "account_id": np.random.choice(accounts["account_id"], n_limits),
            "limit_type": np.random.choice(
                ["daily", "monthly", "transaction"], n_limits
            ),
            "limit_amount": np.round(np.random.uniform(100, 10000, n_limits), 2),
            "effective_date": [
                datetime(2023, 1, 1) + timedelta(days=int(d))
                for d in np.random.randint(0, 730, n_limits)
            ],
        }
    )

    return {
        "accounts": accounts,
        "merchants": merchants,
        "transactions": transactions,
        "limits": limits,
    }
