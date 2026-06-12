"""
Generate professional dark-theme healthcare pipeline charts.
Reads pipeline CSVs and outputs PNGs to the visuals/ directory.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ---------- paths ----------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "visuals")

claims_raw = pd.read_csv(os.path.join(BASE, "data", "raw", "claims_source_2025_q1.csv"))
claims_clean = pd.read_csv(os.path.join(BASE, "data", "processed", "claims_clean.csv"))
dashboard = pd.read_csv(os.path.join(BASE, "exports", "tableau_pipeline_dashboard_extract.csv"))
audit = pd.read_csv(os.path.join(BASE, "exports", "pipeline_audit_summary.csv"))

# ---------- style ----------
BG = "#1a1a2e"
CARD = "#16213e"
ACCENT = ["#0ea5e9", "#22d3ee", "#a78bfa", "#f472b6", "#34d399", "#fbbf24"]
plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": CARD,
    "axes.edgecolor": "#334155",
    "axes.labelcolor": "#e2e8f0",
    "xtick.color": "#94a3b8",
    "ytick.color": "#94a3b8",
    "text.color": "#e2e8f0",
    "grid.color": "#1e293b",
    "grid.alpha": 0.6,
    "font.family": "sans-serif",
    "font.size": 11,
})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  saved {name}")


# ============================================================
# Chart 1 - Pipeline Data Flow (volume at each stage)
# ============================================================
row = audit.iloc[0]
stages = ["Raw Claims\nIngested", "Clean Claims\nValidated", "Providers\nLoaded", "Dashboard\nExport Rows"]
values = [int(row["raw_claim_rows"]), int(row["clean_claim_rows"]),
          int(row["provider_rows"]), int(row["dashboard_extract_rows"])]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(stages, values, color=ACCENT[:4], width=0.55, edgecolor="none")
for b, v in zip(bars, values):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 80,
            f"{v:,}", ha="center", va="bottom", fontweight="bold", fontsize=13, color="#e2e8f0")
ax.set_title("Pipeline Data Flow  |  Record Volume by Stage", fontsize=15, fontweight="bold", pad=14)
ax.set_ylabel("Record Count")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_ylim(0, max(values) * 1.18)
ax.grid(axis="y", linestyle="--")
save(fig, "pipeline_data_flow.png")


# ============================================================
# Chart 2 - Data Quality: Raw vs Clean comparison
# ============================================================
raw_nulls_pct = claims_raw.isnull().mean().mean() * 100
clean_nulls_pct = claims_clean.isnull().mean().mean() * 100
raw_cols = len(claims_raw.columns)
clean_cols = len(claims_clean.columns)

metrics = ["Completeness\nRate (%)", "Schema\nColumns", "Enrichment\nFields Added"]
raw_vals = [100 - raw_nulls_pct, raw_cols, 0]
clean_vals = [100 - clean_nulls_pct, clean_cols, clean_cols - raw_cols]

fig, axes = plt.subplots(1, 3, figsize=(12, 4.5))
for i, (m, rv, cv) in enumerate(zip(metrics, raw_vals, clean_vals)):
    ax = axes[i]
    x = [0, 1]
    ax.bar(x, [rv, cv], color=[ACCENT[4], ACCENT[0]], width=0.45, edgecolor="none")
    ax.set_xticks(x)
    ax.set_xticklabels(["Raw", "Clean"], fontsize=11)
    ax.set_title(m, fontsize=12, fontweight="bold", pad=8)
    for xi, v in zip(x, [rv, cv]):
        label = f"{v:.1f}" if isinstance(v, float) else str(int(v))
        ax.text(xi, v + max(rv, cv) * 0.04, label, ha="center", fontweight="bold",
                fontsize=12, color="#e2e8f0")
    ax.set_ylim(0, max(rv, cv) * 1.22)
    ax.grid(axis="y", linestyle="--")
fig.suptitle("Data Quality  |  Raw vs. Cleaned Dataset Comparison",
             fontsize=14, fontweight="bold", y=1.02)
fig.tight_layout()
save(fig, "data_quality_comparison.png")


# ============================================================
# Chart 3 - Claims KPIs by Payer
# ============================================================
payer_stats = dashboard.groupby("payer").agg(
    total_claims=("total_claims", "sum"),
    approved=("approved_claims", "sum"),
    denied=("denied_claims", "sum"),
    paid=("paid_amount", "sum"),
    billed=("billed_amount", "sum"),
).reset_index()
payer_stats["approval_rate"] = payer_stats["approved"] / payer_stats["total_claims"] * 100
payer_stats["denial_rate"] = payer_stats["denied"] / payer_stats["total_claims"] * 100
payer_stats = payer_stats.sort_values("total_claims", ascending=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# left: horizontal bar - claim volume
ax1.barh(payer_stats["payer"], payer_stats["total_claims"], color=ACCENT[0], height=0.5)
for y, v in zip(range(len(payer_stats)), payer_stats["total_claims"]):
    ax1.text(v + 15, y, f"{v:,}", va="center", fontweight="bold", fontsize=11, color="#e2e8f0")
ax1.set_title("Total Claims by Payer", fontsize=13, fontweight="bold", pad=10)
ax1.set_xlabel("Claim Count")
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax1.set_xlim(0, payer_stats["total_claims"].max() * 1.18)
ax1.grid(axis="x", linestyle="--")

# right: grouped bar - approval vs denial rate
x = range(len(payer_stats))
w = 0.35
ax2.bar([i - w/2 for i in x], payer_stats["approval_rate"].values, w,
        label="Approval %", color=ACCENT[4])
ax2.bar([i + w/2 for i in x], payer_stats["denial_rate"].values, w,
        label="Denial %", color=ACCENT[3])
ax2.set_xticks(list(x))
ax2.set_xticklabels(payer_stats["payer"].values, fontsize=9)
ax2.set_ylabel("Rate (%)")
ax2.set_title("Approval vs. Denial Rate by Payer", fontsize=13, fontweight="bold", pad=10)
ax2.legend(frameon=False, fontsize=10)
ax2.grid(axis="y", linestyle="--")

fig.suptitle("Healthcare Claims KPIs by Payer", fontsize=15, fontweight="bold", y=1.02)
fig.tight_layout()
save(fig, "claims_kpis_by_payer.png")


# ============================================================
# Chart 4 - Monthly Cost Trends (Billed vs Paid)
# ============================================================
dashboard["report_month"] = pd.to_datetime(dashboard["report_month"])
monthly = dashboard.groupby("report_month").agg(
    billed=("billed_amount", "sum"),
    paid=("paid_amount", "sum"),
).reset_index().sort_values("report_month")

fig, ax = plt.subplots(figsize=(11, 5))
ax.fill_between(monthly["report_month"], monthly["billed"], alpha=0.25, color=ACCENT[2])
ax.plot(monthly["report_month"], monthly["billed"], color=ACCENT[2], linewidth=2.2,
        marker="o", markersize=5, label="Billed Amount")
ax.fill_between(monthly["report_month"], monthly["paid"], alpha=0.25, color=ACCENT[0])
ax.plot(monthly["report_month"], monthly["paid"], color=ACCENT[0], linewidth=2.2,
        marker="s", markersize=5, label="Paid Amount")
ax.set_title("Monthly Cost Trends  |  Billed vs. Paid Amount", fontsize=15, fontweight="bold", pad=14)
ax.set_ylabel("Amount ($)")
ax.set_xlabel("Report Month")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend(frameon=False, fontsize=11)
ax.grid(axis="both", linestyle="--")
fig.autofmt_xdate(rotation=30)
save(fig, "monthly_cost_trends.png")

print("\nAll charts generated successfully.")
