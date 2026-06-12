-- Project 05: Pipeline analysis queries
-- Purpose: Demonstrate pipeline monitoring and reconciliation thinking.

WITH monthly AS (
    SELECT
        report_month,
        SUM(total_claims) AS total_claims,
        SUM(denied_claims) AS denied_claims,
        SUM(paid_amount) AS paid_amount
    FROM reporting.vw_pipeline_claims_dashboard
    GROUP BY report_month
)
SELECT
    report_month,
    total_claims,
    denied_claims,
    ROUND(100.0 * denied_claims / NULLIF(total_claims, 0), 2) AS denial_rate,
    paid_amount,
    LAG(total_claims) OVER (ORDER BY report_month) AS prior_month_claims,
    total_claims - LAG(total_claims) OVER (ORDER BY report_month) AS claim_volume_change
FROM monthly
ORDER BY report_month;

SELECT
    specialty,
    state,
    SUM(total_claims) AS total_claims,
    ROUND(AVG(denial_rate), 2) AS avg_denial_rate,
    ROUND(SUM(paid_amount), 2) AS total_paid_amount,
    RANK() OVER (ORDER BY AVG(denial_rate) DESC) AS denial_risk_rank
FROM reporting.vw_pipeline_claims_dashboard
GROUP BY specialty, state
ORDER BY denial_risk_rank;

