import pandas as pd
import numpy as np

np.random.seed(42)

n = 2000

# Generate base features
df = pd.DataFrame({
    "customer_id": range(n),
    "snapshot_date": pd.date_range("2024-10-01", periods=n, freq="h"),  # changed 'H' -> 'h'
    "avg_session_30d": np.random.gamma(2, 10, n),
    "actions_7d": np.random.poisson(5, n),
    "actions_30d": np.random.poisson(20, n),
    "days_since_last_login": np.random.randint(0, 60, n),
    "account_age_days": np.random.randint(30, 1000, n),
    "plan_type": np.random.choice(["basic", "premium"], n),
})

# Correlated churn label
# Customers with low activity in last 7 days are more likely to churn
df["churn_label"] = (df["actions_7d"] < 3).astype(int)

# Save to Parquet
df.to_parquet("data/features/churn_features.parquet", index=False)

print("Sample data generated with correlated churn!")
