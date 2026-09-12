"""US-FT-S03 — Bronze Quarantine

First step of the bronze-to-silver pipeline. Removes transactions that fail
basic structural checks before any further transformation.
"""

import pyspark.sql.functions as F
from pyspark.sql import DataFrame


def quarantine(transactions_sdf: DataFrame) -> DataFrame:
    """Remove records with non-positive amounts or missing merchant references."""
    return transactions_sdf.filter(
        (F.col("amount") > 0) & F.col("merchant_id").isNotNull()
    )
