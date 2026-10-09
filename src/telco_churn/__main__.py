"""Run with python -m telco_churn {download,analyze,train,score}."""

import argparse
import hashlib
import json
from pathlib import Path

import duckdb
import joblib
import pandas as pd
import sklearn

from .data import DATA_PATH, ROOT, download_data, load_data
from .model import score, train


def analyze(df, output):
    con = duckdb.connect(":memory:")
    sql_data = df.copy()
    sql_data["Churn"] = sql_data["Churn"].map({1: "Yes", 0: "No"})
    con.register("churn", sql_data)
    for query in sorted((ROOT / "sql").glob("*.sql")):
        con.execute(query.read_text()).df().to_csv(
            output / f"{query.stem}.csv", index=False
        )
    con.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["download", "analyze", "train", "score"])
    parser.add_argument("--data", type=Path, default=DATA_PATH)
    parser.add_argument("--output", type=Path, default=ROOT / "reports")
    parser.add_argument(
        "--model", type=Path, default=ROOT / "reports" / "churn_pipeline.joblib"
    )
    args = parser.parse_args()
    if args.command == "download":
        print(download_data(args.data))
        return
    args.output.mkdir(parents=True, exist_ok=True)
    if args.command == "score":
        scored = score(joblib.load(args.model), pd.read_csv(args.data))
        scored.to_csv(args.output / "customer_churn_risk_scores.csv", index=False)
    else:
        df = load_data(args.data)
        if args.command == "analyze":
            analyze(df, args.output)
        else:
            pipeline, metrics, holdout = train(df)
            metrics["dataset_sha256"] = hashlib.sha256(
                args.data.read_bytes()
            ).hexdigest()
            metrics["versions"] = {
                "scikit-learn": sklearn.__version__,
                "pandas": pd.__version__,
            }
            joblib.dump(pipeline, args.output / "churn_pipeline.joblib")
            (args.output / "model_metrics.json").write_text(
                json.dumps(metrics, indent=2) + "\n"
            )
            holdout.to_csv(args.output / "holdout_predictions.csv", index=False)
            score(pipeline, df).to_csv(
                args.output / "customer_churn_risk_scores.csv", index=False
            )
            print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
