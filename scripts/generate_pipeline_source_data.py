"""Generate synthetic source files for Project 05 healthcare analytics pipeline."""

from __future__ import annotations

from pathlib import Path
import random

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"


def main() -> None:
    random.seed(125)
    np.random.seed(125)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    providers = pd.DataFrame(
        {
            "provider_id": [f"PRV-{i:04d}" for i in range(3001, 3061)],
            "specialty": np.random.choice(["Primary Care", "Cardiology", "Orthopedics", "Radiology"], size=60),
            "state": np.random.choice(["TX", "FL", "GA", "NC", "AZ"], size=60),
        }
    )

    claims = pd.DataFrame(
        {
            "claim_id": [f"PIPE-CLM-{i:06d}" for i in range(1, 5001)],
            "provider_id": np.random.choice(providers["provider_id"], size=5000),
            "payer": np.random.choice(["Medicare", "Medicaid", "Commercial", "Medicare Advantage"], size=5000),
            "claim_status": np.random.choice(["Approved", "Denied", "Pending"], size=5000, p=[0.76, 0.14, 0.10]),
            "service_date": np.random.choice(pd.date_range("2024-01-01", "2025-03-31"), size=5000),
            "billed_amount": np.round(np.random.lognormal(7.0, 0.5, size=5000), 2),
            "allowed_amount": np.round(np.random.lognormal(6.4, 0.45, size=5000), 2),
        }
    )
    claims["paid_amount"] = np.where(
        claims["claim_status"].eq("Denied"),
        0,
        np.round(claims["allowed_amount"] * np.random.uniform(0.72, 0.97, size=len(claims)), 2),
    )
    claims["load_file_name"] = "claims_source_2025_q1.csv"

    providers.to_csv(RAW_DIR / "providers_source.csv", index=False)
    claims.to_csv(RAW_DIR / "claims_source_2025_q1.csv", index=False)
    print(f"Wrote source files to {RAW_DIR}")


if __name__ == "__main__":
    main()

