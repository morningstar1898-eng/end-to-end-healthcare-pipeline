"""Run a lightweight end-to-end healthcare analytics pipeline.

Flow:
raw CSV files -> pandas cleaning -> processed CSV outputs -> dashboard extracts

PostgreSQL loading is documented in sql/01_schema.sql and can be done with
COPY commands or pgAdmin import after running this script.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import logging

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
EXPORT_DIR = PROJECT_DIR / "exports"
LOG_DIR = PROJECT_DIR / "logs"


def setup_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / "pipeline_run.log"
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    logging.info("Pipeline started")


def validate_required_columns(df: pd.DataFrame, required: set[str], dataset_name: str) -> None:
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{dataset_name} is missing required columns: {sorted(missing)}")


def clean_claims(claims: pd.DataFrame) -> pd.DataFrame:
    required = {
        "claim_id",
        "provider_id",
        "payer",
        "claim_status",
        "service_date",
        "billed_amount",
        "allowed_amount",
        "paid_amount",
    }
    validate_required_columns(claims, required, "claims")
    claims = claims.copy()
    claims["service_date"] = pd.to_datetime(claims["service_date"], errors="coerce")
    amount_cols = ["billed_amount", "allowed_amount", "paid_amount"]
    for col in amount_cols:
        claims[col] = pd.to_numeric(claims[col], errors="coerce").fillna(0)
        claims[col] = claims[col].clip(lower=0)
    claims["claim_status"] = claims["claim_status"].str.title().fillna("Unknown")
    claims["report_month"] = claims["service_date"].dt.to_period("M").dt.to_timestamp()
    claims["denied_flag"] = claims["claim_status"].eq("Denied").astype(int)
    claims["approved_flag"] = claims["claim_status"].eq("Approved").astype(int)
    return claims.drop_duplicates(subset=["claim_id"])


def clean_providers(providers: pd.DataFrame) -> pd.DataFrame:
    required = {"provider_id", "specialty", "state"}
    validate_required_columns(providers, required, "providers")
    providers = providers.copy()
    providers["specialty"] = providers["specialty"].fillna("Unknown")
    providers["state"] = providers["state"].fillna("Unknown")
    return providers.drop_duplicates(subset=["provider_id"])


def create_dashboard_extract(claims: pd.DataFrame, providers: pd.DataFrame) -> pd.DataFrame:
    merged = claims.merge(providers, on="provider_id", how="left")
    extract = (
        merged.groupby(["report_month", "payer", "specialty", "state"], dropna=False)
        .agg(
            total_claims=("claim_id", "count"),
            approved_claims=("approved_flag", "sum"),
            denied_claims=("denied_flag", "sum"),
            billed_amount=("billed_amount", "sum"),
            allowed_amount=("allowed_amount", "sum"),
            paid_amount=("paid_amount", "sum"),
        )
        .reset_index()
    )
    extract["approval_rate"] = extract["approved_claims"] / extract["total_claims"]
    extract["denial_rate"] = extract["denied_claims"] / extract["total_claims"]
    extract["paid_to_allowed_ratio"] = extract["paid_amount"] / extract["allowed_amount"].replace(0, pd.NA)
    return extract


def main() -> None:
    setup_logging()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    run_started_at = datetime.now()
    claims = pd.read_csv(RAW_DIR / "claims_source_2025_q1.csv")
    providers = pd.read_csv(RAW_DIR / "providers_source.csv")
    logging.info("Loaded raw claims rows=%s providers rows=%s", len(claims), len(providers))

    clean_claims_df = clean_claims(claims)
    clean_providers_df = clean_providers(providers)
    extract = create_dashboard_extract(clean_claims_df, clean_providers_df)

    clean_claims_df.to_csv(PROCESSED_DIR / "claims_clean.csv", index=False)
    clean_providers_df.to_csv(PROCESSED_DIR / "providers_clean.csv", index=False)
    extract.to_csv(EXPORT_DIR / "tableau_pipeline_dashboard_extract.csv", index=False)

    audit = pd.DataFrame(
        [
            {
                "run_started_at": run_started_at,
                "run_completed_at": datetime.now(),
                "raw_claim_rows": len(claims),
                "clean_claim_rows": len(clean_claims_df),
                "provider_rows": len(clean_providers_df),
                "dashboard_extract_rows": len(extract),
                "status": "success",
            }
        ]
    )
    audit.to_csv(EXPORT_DIR / "pipeline_audit_summary.csv", index=False)
    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()

