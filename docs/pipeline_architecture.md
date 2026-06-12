# Project 05 Pipeline Architecture

## Business Objective

Build a repeatable healthcare analytics workflow that moves raw CSV data into cleaned files, PostgreSQL reporting views, and Tableau-ready dashboard extracts.

## Pipeline Flow

```text
Raw CSV Files
    -> Python validation and cleaning
    -> Processed CSV outputs
    -> PostgreSQL raw and staging tables
    -> SQL reporting views
    -> Tableau dashboard extract
    -> Executive dashboard and screenshots
```

## Files

```text
scripts/generate_pipeline_source_data.py
scripts/run_healthcare_pipeline.py
sql/01_schema.sql
sql/02_data_quality_checks.sql
sql/03_kpi_views.sql
sql/04_analysis_queries.sql
exports/tableau_pipeline_dashboard_extract.csv
exports/pipeline_audit_summary.csv
logs/pipeline_run.log
```

## Logging and Error Handling

The pipeline script writes run activity to `logs/pipeline_run.log`. Required column validation stops the pipeline when input files do not match expectations. This is intentionally simple but demonstrates professional pipeline thinking: fail early, log clearly, and preserve audit outputs.

## Recruiter Value

This project proves the ability to think like an analytics engineer, not only an analyst. It shows repeatable data preparation, validation, clean outputs, and BI delivery.

