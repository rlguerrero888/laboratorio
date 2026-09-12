from typing import Optional

from data_ai.common.data_generator import generate_fintech_data
from data_ai.common.spark_session import get_spark
from data_ai.config.settings import get_settings
from data_ai.fintech.bronze.ingestor import ingest_transactions


def main() -> None:
    settings = get_settings()
    spark = get_spark()
    data = generate_fintech_data()

    bronze = ingest_transactions(spark, data["transactions"])
    merchants_sdf = spark.createDataFrame(data["merchants"])
    limits_sdf = spark.createDataFrame(data["limits"])
    accounts_sdf = spark.createDataFrame(data["accounts"])

    try:
        from data_ai.fintech.silver.pipeline.build import build_silver_transactions
        silver = build_silver_transactions(bronze, merchants_sdf, limits_sdf)
    except (ImportError, NotImplementedError):
        print("[Gold] build.py not yet created or build_silver_transactions() not implemented")
        return

    from data_ai.fintech.io.storage import write_parquet

    def _run(label: str, module: str, fn_name: str, *args, path: Optional[str] = None) -> None:
        try:
            import importlib
            mod = importlib.import_module(module)
            result = getattr(mod, fn_name)(*args)
            print(f"=== Gold — {label} ===", flush=True)
            result.show(truncate=False)
            if path:
                write_parquet(result, path)
        except (ImportError, NotImplementedError):
            print(f"[Gold] {label}: file not yet created or function not implemented")

    try:
        _run("Spend by Account Type", "data_ai.fintech.gold.spend",
             "spend_by_account_type", silver, accounts_sdf,
             path=f"{settings.storage.gold_path}/spend_by_account_type")
        _run("Top 5 Merchants by Volume", "data_ai.fintech.gold.merchants",
             "top_merchants_by_volume", silver, merchants_sdf,
             path=f"{settings.storage.gold_path}/top_merchants")
        _run("Monthly Transaction Trends", "data_ai.fintech.gold.trends",
             "monthly_transaction_trends", silver,
             path=f"{settings.storage.gold_path}/monthly_trends")
        _run("Decline Rate by Category", "data_ai.fintech.gold.decline",
             "decline_rate_by_category", silver,
             path=f"{settings.storage.gold_path}/decline_rate")
        _run("Category Spend Report", "data_ai.fintech.gold.category_report",
             "category_spend_report", spark, silver, merchants_sdf,
             path=f"{settings.storage.gold_path}/category_report")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
