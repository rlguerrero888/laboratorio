"""Seed the data lake with synthetic fintech data.

Writes Bronze unconditionally. Attempts Silver and Gold but skips gracefully
if the candidate has not yet created those files.

Usage:
    python jobs/seed.py
    make seed
"""

from data_ai.common.data_generator import generate_fintech_data
from data_ai.common.spark_session import get_spark
from data_ai.config.settings import get_settings
from data_ai.fintech.bronze.ingestor import ingest_and_persist


def main() -> None:
    settings = get_settings()
    spark = get_spark("fintech-seed")
    data = generate_fintech_data()

    merchants_sdf = spark.createDataFrame(data["merchants"])
    limits_sdf = spark.createDataFrame(data["limits"])
    accounts_sdf = spark.createDataFrame(data["accounts"])

    # Bronze always succeeds
    bronze = ingest_and_persist(spark, data["transactions"], settings.storage.bronze_path)
    print(f"[seed] Bronze : {bronze.count():,} records → {settings.storage.bronze_path}")

    # Silver
    silver = None
    try:
        from data_ai.fintech.silver.pipeline.build import build_silver_transactions
        from data_ai.fintech.io.storage import write_parquet
        silver = build_silver_transactions(bronze, merchants_sdf, limits_sdf)
        write_parquet(silver, settings.storage.silver_path)
        print(f"[seed] Silver : {silver.count():,} records → {settings.storage.silver_path}")
    except (ImportError, NotImplementedError):
        print("[seed] Silver : skipped — build.py not yet created or not implemented")

    if silver is None:
        return

    from data_ai.fintech.io.storage import write_parquet
    import importlib

    def _seed_gold(label: str, module: str, fn_name: str, *args, path: str) -> None:
        try:
            mod = importlib.import_module(module)
            result = getattr(mod, fn_name)(*args)
            write_parquet(result, path)
            print(f"[seed] Gold/{label} → {path}")
        except (ImportError, NotImplementedError):
            print(f"[seed] Gold/{label}: skipped — file not yet created or not implemented")

    _seed_gold("spend_by_account_type", "data_ai.fintech.gold.spend",
               "spend_by_account_type", silver, accounts_sdf,
               path=f"{settings.storage.gold_path}/spend_by_account_type")
    _seed_gold("top_merchants", "data_ai.fintech.gold.merchants",
               "top_merchants_by_volume", silver, merchants_sdf,
               path=f"{settings.storage.gold_path}/top_merchants")
    _seed_gold("monthly_trends", "data_ai.fintech.gold.trends",
               "monthly_transaction_trends", silver,
               path=f"{settings.storage.gold_path}/monthly_trends")
    _seed_gold("decline_rate", "data_ai.fintech.gold.decline",
               "decline_rate_by_category", silver,
               path=f"{settings.storage.gold_path}/decline_rate")


if __name__ == "__main__":
    main()
