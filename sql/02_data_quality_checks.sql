-- Project 05: Pipeline data quality checks
-- Purpose: Monitor completeness, uniqueness, and valid value ranges.

SELECT COUNT(*) AS raw_claim_rows
FROM raw.pipeline_claims_raw;

SELECT claim_id, COUNT(*) AS duplicate_count
FROM raw.pipeline_claims_raw
GROUP BY claim_id
HAVING COUNT(*) > 1;

SELECT
    SUM(CASE WHEN claim_id IS NULL THEN 1 ELSE 0 END) AS missing_claim_id,
    SUM(CASE WHEN provider_id IS NULL THEN 1 ELSE 0 END) AS missing_provider_id,
    SUM(CASE WHEN service_date IS NULL THEN 1 ELSE 0 END) AS missing_service_date,
    SUM(CASE WHEN payer IS NULL THEN 1 ELSE 0 END) AS missing_payer
FROM raw.pipeline_claims_raw;

SELECT c.provider_id, COUNT(*) AS orphan_claims
FROM raw.pipeline_claims_raw c
LEFT JOIN raw.pipeline_providers_raw p
    ON c.provider_id = p.provider_id
WHERE p.provider_id IS NULL
GROUP BY c.provider_id
ORDER BY orphan_claims DESC;

