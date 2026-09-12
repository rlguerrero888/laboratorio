from data_ai.common.data_generator import generate_fintech_data
from data_ai.common.spark_session import get_spark
from data_ai.config.settings import get_settings
from data_ai.fintech.bronze.ingestor import ingest_transactions


def main() -> None:
    settings = get_settings()
    spark = get_spark()
    data = generate_fintech_data()

    # DQ report
    try:
        from data_ai.fintech.dq.engine import TransactionValidationEngine
        engine = TransactionValidationEngine()
        report = engine.validate(data["transactions"])
        print("=== DQ Report ===")
        print(f"  total      : {report.total_transactions}")
        print(f"  invalid_$  : {report.invalid_amount}")
        print(f"  currency   : {report.unsupported_currency}")
        print(f"  no_merchant: {report.missing_merchant}")
        print(f"  valid      : {report.valid_transactions}")
    except (ImportError, NotImplementedError):
        print("[DQ] engine.py not yet created or validate() not implemented")

    # Bronze → Silver pipeline
    bronze = ingest_transactions(spark, data["transactions"])
    merchants_sdf = spark.createDataFrame(data["merchants"])
    limits_sdf = spark.createDataFrame(data["limits"])

    try:
        from data_ai.fintech.silver.pipeline.build import build_silver_transactions
        from data_ai.fintech.io.storage import write_parquet
        silver = build_silver_transactions(bronze, merchants_sdf, limits_sdf)
        write_parquet(silver, settings.storage.silver_path)
        print(f"\n=== Silver Pipeline ===")
        print(f"  Bronze : {bronze.count():,}  →  Silver : {silver.count():,}")
        print(f"  Written → {settings.storage.silver_path}")
        silver.select(
            "transaction_id", "amount", "category", "country",
            "daily_limit", "exceeds_daily_limit",
        ).show(10, truncate=False)
    except (ImportError, NotImplementedError):
        print("\n[Silver] build.py not yet created or build_silver_transactions() not implemented")


if __name__ == "__main__":
    main()
