"""Shared SparkSession factory.

Reads configuration from settings — supports local mode and S3A (MinIO)
without changing call sites. Set MINIO_ENDPOINT in the environment to
enable S3-compatible storage.
"""

from typing import Optional

from pyspark.sql import SparkSession


def get_spark(app_name: Optional[str] = None) -> SparkSession:
    from data_ai.config.settings import get_settings

    cfg = get_settings().spark
    name = app_name or cfg.app_name

    builder = (
        SparkSession.builder
        .appName(name)
        .master(cfg.master)
        .config("spark.sql.shuffle.partitions", str(cfg.shuffle_partitions))
        .config("spark.ui.enabled", "false")
    )

    if cfg.s3_endpoint:
        builder = (
            builder
            .config("spark.hadoop.fs.s3a.endpoint", cfg.s3_endpoint)
            .config("spark.hadoop.fs.s3a.access.key", cfg.s3_access_key)
            .config("spark.hadoop.fs.s3a.secret.key", cfg.s3_secret_key)
            .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
            .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
            .config("spark.hadoop.fs.s3a.bucket.create.enabled", "true")
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .config("spark.hadoop.fs.s3a.connection.timeout", "60000")
            .config("spark.hadoop.fs.s3a.socket.timeout", "60000")
            .config(
                "spark.jars.packages",
                "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262",
            )
        )

    spark = builder.getOrCreate()

    if cfg.s3_endpoint:
        hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
        hadoop_conf.set("fs.s3a.connection.timeout", "60000")
        hadoop_conf.set("fs.s3a.socket.timeout", "60000")

    return spark
