# Project 05 Tableau Dashboard Spec

## Dashboard Title

End-to-End Healthcare Analytics Pipeline Monitor

## Dashboard Pages

### 1. Pipeline Monitoring Overview

Top KPI cards:

- Raw claim rows
- Clean claim rows
- Dashboard extract rows
- Denial rate
- Approval rate
- Paid-to-allowed percentage

Charts:

- Monthly claim volume trend
- Denial rate by payer
- Paid amount by specialty
- Claims by state

Business question: Did the pipeline produce trusted reporting outputs?

### 2. Data Quality Summary

Charts:

- Missing provider count
- Missing service date count
- Unknown claim status count
- Orphan provider claims
- Row count reconciliation

Business question: Are there data quality issues that could affect reporting confidence?

### 3. Reporting Extract Flow

Charts:

- Raw to clean row count comparison
- Dashboard extract row count by month
- Specialty/state risk ranking
- Pipeline audit table

Business question: Can stakeholders trust the data movement from raw files to dashboard?

## Filters

- Report month
- Payer
- Specialty
- State
- Claim status

## Screenshots Needed

- `project_05_pipeline_monitoring_overview.png`
- `project_05_data_quality_summary.png`
- `project_05_dashboard_extract_flow.png`

