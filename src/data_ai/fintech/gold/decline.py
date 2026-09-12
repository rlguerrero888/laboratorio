import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Window


def decline_rate_by_category(silver_sdf: DataFrame) -> DataFrame:
    """
    Decline rate by merchant category, ranked highest to lowest.
    Result columns: category, total_transactions, declined_count, decline_rate, decline_rank.
    Silver already has category from the enrichment step — no additional join needed.
    """
    by_category = (
        silver_sdf
        .groupBy("category")
        .agg(
            F.count("transaction_id").alias("total_transactions"),
            F.sum(F.when(F.col("status") == "declined", 1).otherwise(0)).alias("declined_count"),
        )
        .withColumn("decline_rate", F.col("declined_count") / F.col("total_transactions"))
        .withColumn("decline_rank", F.rank().over(Window.orderBy(F.col("decline_rate").desc())))
        .orderBy(F.col("decline_rate").desc())
    )

    return by_category.select(
        "category",
        "total_transactions",
        "declined_count",
        F.round("decline_rate", 4).alias("decline_rate"),
        "decline_rank",
    )
