import yaml
import json
import joblib
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score

from features import load_features


def main():
    with open("configs/train.yaml") as f:
        cfg = yaml.safe_load(f)

    df = load_features(cfg["data"]["feature_path"])

    ts_col = cfg["data"]["timestamp_col"]
    target = cfg["data"]["target"]

    train_end = cfg["split"]["train_end_date"]
    val_end = cfg["split"]["val_end_date"]

    train_df = df[df[ts_col] <= train_end]
    val_df = df[(df[ts_col] > train_end) & (df[ts_col] <= val_end)]

    X_train = train_df.drop(columns=[target])
    y_train = train_df[target]

    X_val = val_df.drop(columns=[target])
    y_val = val_df[target]

    categorical = ["plan_type"]
    numerical = [c for c in X_train.columns if c not in categorical + [ts_col]]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", numerical),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ]
    )

    model = GradientBoostingClassifier(**cfg["model"]["params"])

    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", model),
        ]
    )

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict_proba(X_val)[:, 1]

    roc_auc = roc_auc_score(y_val, preds)

    print(f"Validation ROC-AUC: {roc_auc:.4f}")

    if roc_auc < cfg["metrics"]["min_roc_auc"]:
        raise RuntimeError("Model did not meet quality gate")

    output_dir = Path(cfg["artifacts"]["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(pipeline, output_dir / "model.joblib")

    metrics = {
        "roc_auc": roc_auc,
        "n_train": len(X_train),
        "n_val": len(X_val),
    }

    with open(output_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)


if __name__ == "__main__":
    main()
