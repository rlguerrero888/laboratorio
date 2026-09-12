import pyspark.sql.functions as F
from pyspark.sql import DataFrame


def top_merchants_by_volume(
    silver_sdf: DataFrame, merchants_sdf: DataFrame, top_n: int = 5
) -> DataFrame:
    """
    Top N merchants by transaction volume, excluding declined transactions.
    Result columns: merchant_id, name, category, total_transactions, total_amount.
    """
    merchant_ref = merchants_sdf.select("merchant_id", "name")

    return (
        silver_sdf
        .filter(F.col("status") != "declined")
        .join(merchant_ref, on="merchant_id", how="left")
        .groupBy("merchant_id", "name", "category")
        .agg(
            F.count("transaction_id").alias("total_transactions"),
            F.round(F.sum("amount"), 2).alias("total_amount"),
        )
        .orderBy(F.col("total_amount").desc(), F.col("total_transactions").desc())
        .limit(top_n)
    )
