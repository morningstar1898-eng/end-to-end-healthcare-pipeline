-- Project 05: End-to-End Healthcare Analytics Pipeline
-- Purpose: Create database objects for raw-to-reporting pipeline delivery.

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS reporting;

DROP TABLE IF EXISTS raw.pipeline_claims_raw;
DROP TABLE IF EXISTS raw.pipeline_providers_raw;

CREATE TABLE raw.pipeline_claims_raw (
    claim_id TEXT PRIMARY KEY,
    provider_id TEXT,
    payer TEXT,
    claim_status TEXT,
    service_date DATE,
    billed_amount NUMERIC(12,2),
    allowed_amount NUMERIC(12,2),
    paid_amount NUMERIC(12,2),
    load_file_name TEXT
);

CREATE TABLE raw.pipeline_providers_raw (
    provider_id TEXT PRIMARY KEY,
    specialty TEXT,
    state TEXT
);

DROP TABLE IF EXISTS staging.pipeline_claims_clean;

CREATE TABLE staging.pipeline_claims_clean AS
SELECT
    claim_id,
    provider_id,
    COALESCE(payer, 'Unknown') AS payer,
    INITCAP(COALESCE(claim_status, 'Unknown')) AS claim_status,
    service_date,
    GREATEST(COALESCE(billed_amount, 0), 0) AS billed_amount,
    GREATEST(COALESCE(allowed_amount, 0), 0) AS allowed_amount,
    GREATEST(COALESCE(paid_amount, 0), 0) AS paid_amount,
    DATE_TRUNC('month', service_date)::DATE AS report_month,
    load_file_name,
    CURRENT_TIMESTAMP AS transformed_at
FROM raw.pipeline_claims_raw;

