import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Window


def monthly_transaction_trends(silver_sdf: DataFrame) -> DataFrame:
    """
    Monthly transaction count and amount with a prev_month_count column (lag of prior month).
    Result ordered chronologically.
    """
    monthly = (
        silver_sdf
        .withColumn("month", F.date_format(F.to_date("transaction_date"), "yyyy-MM"))
        .groupBy("month")
        .agg(
            F.count("transaction_id").alias("transaction_count"),
            F.round(F.sum("amount"), 2).alias("total_amount"),
        )
        .orderBy(F.col("month").asc())
    )

    return monthly.withColumn(
        "prev_month_count",
        F.lag("transaction_count").over(Window.orderBy("month")),
    )
