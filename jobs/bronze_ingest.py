from data_ai.common.data_generator import generate_fintech_data
from data_ai.common.spark_session import get_spark
from data_ai.config.settings import get_settings
from data_ai.fintech.bronze.ingestor import ingest_and_persist


def main() -> None:
    settings = get_settings()
    spark = get_spark()
    data = generate_fintech_data()

    bronze = ingest_and_persist(spark, data["transactions"], settings.storage.bronze_path)
    print(f"[bronze] {bronze.count():,} records written → {settings.storage.bronze_path}")
    bronze.printSchema()


if __name__ == "__main__":
    main()
