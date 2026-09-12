"""Application settings loaded from environment variables.

Defaults target local development. Set environment variables in docker-compose
or .env to point at MinIO / a real data lake.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StorageConfig:
    bronze_path: str = field(default_factory=lambda: os.getenv("BRONZE_PATH", "data/bronze"))
    silver_path: str = field(default_factory=lambda: os.getenv("SILVER_PATH", "data/silver"))
    gold_path: str = field(default_factory=lambda: os.getenv("GOLD_PATH", "data/gold"))


@dataclass
class SparkConfig:
    master: str = field(default_factory=lambda: os.getenv("SPARK_MASTER", "local[*]"))
    app_name: str = field(default_factory=lambda: os.getenv("SPARK_APP_NAME", "fintech-platform"))
    shuffle_partitions: int = field(
        default_factory=lambda: int(os.getenv("SPARK_SHUFFLE_PARTITIONS", "4"))
    )
    # MinIO / S3-compatible endpoint — None means local filesystem
    s3_endpoint: Optional[str] = field(default_factory=lambda: os.getenv("MINIO_ENDPOINT"))
    s3_access_key: str = field(
        default_factory=lambda: os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    )
    s3_secret_key: str = field(
        default_factory=lambda: os.getenv("MINIO_SECRET_KEY", "minioadmin")
    )


@dataclass
class Settings:
    storage: StorageConfig = field(default_factory=StorageConfig)
    spark: SparkConfig = field(default_factory=SparkConfig)


def get_settings() -> Settings:
    return Settings()
