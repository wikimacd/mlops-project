import pandas as pd

def load_features(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)

    required_cols = {
        "avg_session_30d",
        "actions_7d",
        "actions_30d",
        "days_since_last_login",
        "account_age_days",
        "plan_type",
        "snapshot_date",
        "churn_label",
    }

    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    return df
