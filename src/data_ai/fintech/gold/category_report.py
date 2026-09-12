from pyspark.sql import DataFrame, SparkSession


def category_spend_report(
    spark: SparkSession,
    silver_sdf: DataFrame,
    merchants_sdf: DataFrame,
) -> DataFrame:
    """
    Total spend and transaction count per merchant category for approved transactions only.
    Result columns: category, transaction_count, total_spend.
    Ordered by total_spend descending.

    Must be implemented using spark.sql():
      - register silver_sdf as a temp view named 'silver'
      - register merchants_sdf as a temp view named 'merchants'
      - write and return a SQL query
    """
    silver_sdf.createOrReplaceTempView("silver")
    merchants_sdf.createOrReplaceTempView("merchants")

    query = """
        SELECT
            m.category,
            COUNT(s.transaction_id) AS transaction_count,
            ROUND(SUM(s.amount), 2) AS total_spend
        FROM silver s
        JOIN merchants m ON s.merchant_id = m.merchant_id
        WHERE s.status = 'approved'
        GROUP BY m.category
        ORDER BY total_spend DESC
    """
    return spark.sql(query)
