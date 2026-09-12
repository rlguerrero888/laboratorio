from pyspark.sql import DataFrame


def enrich_with_merchant(transactions_sdf: DataFrame, merchants_sdf: DataFrame) -> DataFrame:
    """Adds category and country to each transaction via a merchant join."""
    merchant_ref = merchants_sdf.select("merchant_id", "category", "country")
    return transactions_sdf.join(merchant_ref, on="merchant_id", how="left")
