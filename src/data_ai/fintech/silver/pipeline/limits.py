import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Window


def enrich_with_limits(transactions_sdf: DataFrame, limits_sdf: DataFrame) -> DataFrame:
    """
    Joins the most recent daily limit per account_id.
    Adds columns: daily_limit, exceeds_daily_limit (bool).
    Accounts with no daily limit record must have exceeds_daily_limit = False.
    """
    daily_limits = (
        limits_sdf
        .filter(F.col("limit_type") == "daily")
        .select("account_id", "limit_amount", "effective_date")
        .withColumn("effective_date_ts", F.to_timestamp("effective_date"))
        .withColumn(
            "rn",
            F.row_number().over(
                Window.partitionBy("account_id").orderBy(F.col("effective_date_ts").desc())
            ),
        )
        .filter(F.col("rn") == 1)
        .drop("effective_date", "effective_date_ts", "rn")
        .withColumnRenamed("limit_amount", "daily_limit")
    )

    enriched = transactions_sdf.join(daily_limits, on="account_id", how="left")

    return enriched.withColumn(
        "exceeds_daily_limit",
        F.when(F.col("daily_limit").isNull(), F.lit(False)).otherwise(
            F.col("amount") > F.col("daily_limit")
        ),
    )
