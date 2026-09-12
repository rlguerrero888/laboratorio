"""US-FT-G01 — Spend by Account Type

Aggregates approved transaction spend and count grouped by account type.
Reads from the silver transactions layer joined with the accounts reference table.
"""

import pyspark.sql.functions as F
from pyspark.sql import DataFrame


def spend_by_account_type(silver_sdf: DataFrame, accounts_sdf: DataFrame) -> DataFrame:
    """Return total spend and transaction count per account type for approved transactions."""
    return (
        silver_sdf
        .filter(F.col("status") == "approved")
        .join(accounts_sdf.select("account_id", "account_type"), on="account_id", how="left")
        .groupBy("account_type")
        .agg(
            F.round(F.sum("amount"), 2).alias("total_spend"),
            F.count("transaction_id").alias("transaction_count"),
        )
        .orderBy(F.col("total_spend").desc())
    )
