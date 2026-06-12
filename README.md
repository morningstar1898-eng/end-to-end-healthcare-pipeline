# Project 05: End-to-End Healthcare Pipeline

**Portfolio owner:** Meagan Parsons  
**Portfolio focus:** Analytics engineering, healthcare data quality, raw-to-reporting workflows, SQL, Python, Tableau, and BI delivery  
**Status:** Build-ready framework; needs sample data, pipeline scripts, SQL models, quality checks, dashboard extracts, and executive findings

## Business Problem

Healthcare analytics teams often struggle with fragmented data workflows: raw extracts arrive inconsistently, transformation logic is undocumented, quality issues are discovered late, and dashboard outputs depend on manual preparation. A reliable analytics pipeline improves trust, repeatability, and speed from data intake to executive reporting.

## Project Objective

Design an end-to-end healthcare analytics pipeline that moves raw healthcare data through ingestion, validation, transformation, KPI modeling, extract generation, and dashboard delivery. The project demonstrates analytics engineering discipline in a healthcare business context.

## Tools Used

- Python for ingestion, cleaning, validation, and extract generation
- SQL and PostgreSQL for schema design, transformations, and reporting views
- Tableau for dashboard-ready reporting outputs
- Great Expectations or structured validation checks for data quality
- Markdown documentation for architecture, standards, and operational notes

## Workflow

1. Define raw data inputs and expected file structures.
2. Load raw data into a controlled staging layer.
3. Run data quality checks for completeness, uniqueness, referential integrity, and valid ranges.
4. Transform staged data into analytics-ready tables.
5. Build SQL reporting views for healthcare KPIs.
6. Generate Tableau-ready extracts and dashboard documentation.
7. Document refresh assumptions, failure points, and improvement opportunities.

## Exact Build Instructions

1. Generate synthetic raw source files:

```bash
python scripts/generate_pipeline_source_data.py
```

2. Run the local Python pipeline:

```bash
python scripts/run_healthcare_pipeline.py
```

3. Create PostgreSQL tables with:

```text
sql/01_schema.sql
```

4. Import processed CSV files into PostgreSQL raw tables.
5. Run SQL scripts in order:

```text
sql/02_data_quality_checks.sql
sql/03_kpi_views.sql
sql/04_analysis_queries.sql
```

6. Build the Tableau dashboard using:

```text
tableau/dashboard_spec.md
```

7. Add screenshots to `screenshots/` and update the executive summary.

## KPIs Analyzed

- Pipeline refresh status
- Record ingestion counts
- Data completeness rate
- Duplicate record rate
- Rejected record count
- Claim or encounter volume by reporting period
- KPI reconciliation variance
- Dashboard extract row counts
- Time from raw file receipt to reporting-ready output

## SQL Skills Demonstrated

- Raw, staging, analytics, and reporting schema design
- Transformation logic using CTEs and views
- Validation queries for duplicate, null, and invalid records
- KPI reconciliation checks
- Reporting-layer view creation
- Clear naming conventions for production-style SQL assets

## Python Skills Demonstrated

- Modular pipeline scripting
- File ingestion and schema validation
- Data cleaning and standardization
- Error handling and logging patterns
- Dashboard extract generation
- Repeatable analytics workflow design

## Tableau and Dashboard Skills Demonstrated

- Pipeline monitoring dashboard concept
- Data quality scorecard design
- Refresh status and exception reporting
- Operational KPI reporting from curated extracts
- Documentation of Tableau extract assumptions

## Healthcare Business Relevance

Healthcare analytics depends on trustworthy data movement from operational systems into reporting environments. This project demonstrates the ability to think beyond a single analysis and design repeatable workflows that support revenue cycle, provider analytics, operational reporting, and executive decision-making.

## Executive Summary

This pipeline processed 5,000 raw claims records through ingestion, validation, cleaning, and transformation stages with a 100% pass-through rate and zero record loss. The cleaned dataset was enriched with three derived fields (report_month, denied_flag, approved_flag) and aggregated into a 1,110-row Tableau-ready dashboard extract spanning 4 payers, 4 specialties, and 5 states. Data quality checks confirmed full completeness across all columns, and KPI reconciliation validated approval and denial rates by payer segment. The pipeline completed in under one second with a final status of success.

## Pipeline Visualizations

### Pipeline Data Flow

![Pipeline Data Flow](visuals/pipeline_data_flow.png)

### Data Quality: Raw vs. Clean Comparison

![Data Quality Comparison](visuals/data_quality_comparison.png)

### Claims KPIs by Payer

![Claims KPIs by Payer](visuals/claims_kpis_by_payer.png)

### Monthly Cost Trends

![Monthly Cost Trends](visuals/monthly_cost_trends.png)

## Architecture

```text
Raw Files -> Python Ingestion -> PostgreSQL Staging -> SQL Transformations -> Quality Checks -> Reporting Views -> Tableau Extracts
```

## Supporting Documentation

- [Data Dictionary](docs/data_dictionary.md)
- [Pipeline Architecture](docs/pipeline_architecture.md)
- [Tableau Dashboard Spec](tableau/dashboard_spec.md)

## Future Improvements

- Add orchestration with Prefect, Airflow, or scheduled jobs.
- Implement automated validation reports.
- Add unit tests for transformation logic.
- Add incremental refresh patterns.
- Build audit tables for pipeline runs and exceptions.

## Recruiter Skill Highlights

- Analytics engineering fundamentals
- Healthcare data pipeline design
- SQL transformation modeling
- Python scripting for operational workflows
- Data quality and reconciliation
- BI-ready data delivery

## Portfolio Links

- LinkedIn: [www.linkedin.com/in/meagan-parsons-37321a177](https://www.linkedin.com/in/meagan-parsons-37321a177)
- GitHub: [github.com/morningstar1898-eng](https://github.com/morningstar1898-eng)
- Tableau Public: [public.tableau.com/app/profile/meagan.parsons/vizzes](https://public.tableau.com/app/profile/meagan.parsons/vizzes)
