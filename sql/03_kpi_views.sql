-- Project 05: Reporting views
-- Purpose: Transform clean claims and provider data into BI-ready KPI views.

CREATE OR REPLACE VIEW reporting.vw_pipeline_claims_dashboard AS
SELECT
    c.report_month,
    c.payer,
    COALESCE(p.specialty, 'Unknown') AS specialty,
    COALESCE(p.state, 'Unknown') AS state,
    COUNT(*) AS total_claims,
    SUM(CASE WHEN c.claim_status = 'Approved' THEN 1 ELSE 0 END) AS approved_claims,
    SUM(CASE WHEN c.claim_status = 'Denied' THEN 1 ELSE 0 END) AS denied_claims,
    ROUND(100.0 * SUM(CASE WHEN c.claim_status = 'Approved' THEN 1 ELSE 0 END) / COUNT(*), 2) AS approval_rate,
    ROUND(100.0 * SUM(CASE WHEN c.claim_status = 'Denied' THEN 1 ELSE 0 END) / COUNT(*), 2) AS denial_rate,
    ROUND(SUM(c.billed_amount), 2) AS billed_amount,
    ROUND(SUM(c.allowed_amount), 2) AS allowed_amount,
    ROUND(SUM(c.paid_amount), 2) AS paid_amount,
    ROUND(100.0 * SUM(c.paid_amount) / NULLIF(SUM(c.allowed_amount), 0), 2) AS paid_to_allowed_pct
FROM staging.pipeline_claims_clean c
LEFT JOIN raw.pipeline_providers_raw p
    ON c.provider_id = p.provider_id
GROUP BY c.report_month, c.payer, COALESCE(p.specialty, 'Unknown'), COALESCE(p.state, 'Unknown');

CREATE OR REPLACE VIEW reporting.vw_pipeline_quality_summary AS
SELECT
    load_file_name,
    COUNT(*) AS clean_claim_rows,
    SUM(CASE WHEN provider_id IS NULL THEN 1 ELSE 0 END) AS missing_provider_rows,
    SUM(CASE WHEN service_date IS NULL THEN 1 ELSE 0 END) AS missing_service_date_rows,
    SUM(CASE WHEN claim_status = 'Unknown' THEN 1 ELSE 0 END) AS unknown_status_rows,
    CURRENT_TIMESTAMP AS quality_checked_at
FROM staging.pipeline_claims_clean
GROUP BY load_file_name;

