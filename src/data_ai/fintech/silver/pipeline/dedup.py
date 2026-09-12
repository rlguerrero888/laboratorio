import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Window


def dedup(transactions_sdf: DataFrame) -> DataFrame:
    """
    Removes duplicate transaction_ids, keeping the record
    with the earliest transaction_date.
    """
    deduped = (
        transactions_sdf
        .withColumn("transaction_date_ts", F.to_timestamp("transaction_date"))
        .withColumn(
            "rn",
            F.row_number().over(
                Window.partitionBy("transaction_id").orderBy(F.col("transaction_date_ts").asc())
            ),
        )
        .filter(F.col("rn") == 1)
        .drop("rn", "transaction_date_ts")
    )
    return deduped
