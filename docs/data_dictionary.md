# Project 05 Data Dictionary

## Claims Source

| Field | Description | Example |
| --- | --- | --- |
| `claim_id` | Synthetic claim identifier | `PIPE-CLM-000001` |
| `provider_id` | Synthetic provider identifier | `PRV-3001` |
| `payer` | Payer category | `Medicare Advantage` |
| `claim_status` | Claim adjudication status | `Approved` |
| `service_date` | Date of service | `2025-01-15` |
| `billed_amount` | Submitted charge amount | `1190.00` |
| `allowed_amount` | Allowed amount | `760.00` |
| `paid_amount` | Paid amount | `690.00` |
| `load_file_name` | Source file lineage | `claims_source_2025_q1.csv` |

## Provider Source

| Field | Description | Example |
| --- | --- | --- |
| `provider_id` | Synthetic provider identifier | `PRV-3001` |
| `specialty` | Provider specialty | `Radiology` |
| `state` | Provider state | `TX` |

