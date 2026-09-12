"""Persistence helpers for the data lake.

Abstracts read/write so pipeline steps don't care whether storage is
local Parquet, MinIO (S3A), or any other backend — only the path changes.
"""

from pyspark.sql import DataFrame, SparkSession


def write_parquet(df: DataFrame, path: str, mode: str = "overwrite") -> None:
    """Write a Spark DataFrame to Parquet at the given lake path."""
    writer = df.write.mode(mode)
    if path.startswith("s3a://"):
        writer = writer.option("fs.s3a.bucket.create.enabled", "true")
    writer.parquet(path)


def read_parquet(spark: SparkSession, path: str) -> DataFrame:
    """Read a Parquet dataset from the given lake path."""
    return spark.read.parquet(path)
