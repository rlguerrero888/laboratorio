"""US-FT-B01 — Bronze Transaction Ingestor

Loads raw transaction records into the bronze layer with schema enforcement only.
Bronze preserves source fidelity — no filtering, deduplication, or transformation.
Writes the result to the configured bronze storage path.
"""

import pandas as pd
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import DoubleType, StringType, StructField, StructType

TRANSACTION_SCHEMA = StructType([
    StructField("transaction_id", StringType(), True),
    StructField("account_id", StringType(), True),
    StructField("merchant_id", StringType(), True),
    StructField("transaction_date", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("currency", StringType(), True),
    StructField("transaction_type", StringType(), True),
    StructField("status", StringType(), True),
])


def ingest_transactions(spark: SparkSession, raw_df: pd.DataFrame) -> DataFrame:
    """Load raw transaction records into the bronze layer with schema enforcement."""
    return spark.createDataFrame(raw_df, schema=TRANSACTION_SCHEMA)


def ingest_and_persist(spark: SparkSession, raw_df: pd.DataFrame, bronze_path: str) -> DataFrame:
    """Ingest transactions and write to the bronze storage path."""
    from data_ai.fintech.io.storage import write_parquet
    bronze = ingest_transactions(spark, raw_df)
    write_parquet(bronze, bronze_path)
    return bronze
