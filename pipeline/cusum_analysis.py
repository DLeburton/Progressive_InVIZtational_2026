"""
CUSUM Analysis 
Detects statistically significant shifts in Waymo's monthly crash injury rate.
"""

import sqlite3
import pandas as pd
import numpy as np
import os

# ── Load data ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "waymo_tnc.db")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("""
    SELECT year_month,
           COUNT(*) as total,
           SUM(is_any_injury_reported) as injuries
    FROM cleaned_crashes
    GROUP BY year_month
    ORDER BY year_month
""", conn)
conn.close()

df['injury_rate'] = df['injuries'] / df['total']
df = df[df['total'] >= 20].reset_index(drop=True)

# ── CUSUM parameters ───────────────────────────────────────
# Baseline: mean and std dev of the full filtered series
mu0   = df['injury_rate'].mean()   # target (baseline) mean
sigma = df['injury_rate'].std()    # process std dev
k = 0.0   # c=0: prioritize early detection over false positive risk
h = 3.0 * sigma   # was 4.0                # decision threshold (4-sigma sensitivity)

# ── Two-sided CUSUM ────────────────────────────────────────
# Upper CUSUM: detects upward shift   (injury rate worsening)
# Lower CUSUM: detects downward shift (injury rate improving)
n = len(df)
C_upper = np.zeros(n)
C_lower = np.zeros(n)

for i in range(1, n):
    x = df['injury_rate'].iloc[i]
    C_upper[i] = max(0, C_upper[i-1] + (x - mu0 - k))
    C_lower[i] = max(0, C_lower[i-1] + (mu0 - x - k))

df['cusum_upper'] = C_upper
df['cusum_lower'] = C_lower
df['signal_upper'] = C_upper > h
df['signal_lower'] = C_lower > h

# ── Results ────────────────────────────────────────────────
upper_signals = df[df['signal_upper']]['year_month'].tolist()
lower_signals = df[df['signal_lower']]['year_month'].tolist()

print("=" * 50)
print("CUSUM ANALYSIS — Waymo Injury Rate")
print("=" * 50)
print(f"Usable months (n≥20):  {len(df)}")
print(f"Baseline mean:         {mu0:.4f}  ({mu0*100:.1f}%)")
print(f"Std dev (sigma):       {sigma:.4f}")
print(f"Allowance (k):         {k:.4f}")
print(f"Threshold (h):         {h:.4f}")
print()
print(f"Upward shift signals   (worsening): {upper_signals if upper_signals else 'None'}")
print(f"Downward shift signals (improving): {lower_signals if lower_signals else 'None'}")
if lower_signals:
    print(f"\n>>> First detectable improvement: {lower_signals[0]}")
print("=" * 50)

# ── Save results ───────────────────────────────────────────
out_path = os.path.join(BASE_DIR, "pipeline", "cusum_results.csv")
df.to_csv(out_path, index=False)
print(f"Results saved to pipeline/cusum_results.csv")
