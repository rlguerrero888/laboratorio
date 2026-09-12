from pyspark.sql import DataFrame

from data_ai.fintech.silver.pipeline.dedup import dedup
from data_ai.fintech.silver.pipeline.enrichment import enrich_with_merchant
from data_ai.fintech.silver.pipeline.limits import enrich_with_limits
from data_ai.fintech.silver.pipeline.quarantine import quarantine


def build_silver_transactions(
    transactions_sdf: DataFrame,
    merchants_sdf: DataFrame,
    limits_sdf: DataFrame,
) -> DataFrame:
    """
    Orchestrates the full pipeline:
    quarantine → dedup → enrich_with_merchant → enrich_with_limits
    """
    cleaned = quarantine(transactions_sdf)
    deduped = dedup(cleaned)
    enriched = enrich_with_merchant(deduped, merchants_sdf)
    return enrich_with_limits(enriched, limits_sdf)
