# Model training and inference

## Generate the complete model

```bash
python -m pip install -e ".[dev]"
python -m telco_churn download
python -m telco_churn train
```

Outputs in `reports/`:

- `churn_pipeline.joblib`: one-hot encoders, numeric imputer, scaler, and selected estimator together.
- `model_metrics.json`: training-only CV results, final holdout metrics, seed, dataset checksum, and versions.
- `holdout_predictions.csv`: predictions on the untouched evaluation subset.
- `customer_churn_risk_scores.csv`: all customers scored, with tiers, modeled monthly exposure, and suggested actions. This file includes training customers; do not use it to estimate generalization.

The old `best_churn_model.pkl` and `feature_scaler.pkl` files are obsolete and are not used by this workflow. Retrain to generate a complete pipeline.

## Score new records

Use a CSV with the same original 19 customer feature columns. The target Churn is optional. Unknown categorical values are supported; malformed numeric values and missing feature columns are rejected.

```bash
python -m telco_churn score --data /path/to/customers.csv --model reports/churn_pipeline.joblib --output /path/to/scoring-output
```

Or call the shared Python API:

```python
import joblib
import pandas as pd
from telco_churn.model import score

pipeline = joblib.load('reports/churn_pipeline.joblib')
scores = score(pipeline, pd.read_csv('/path/to/customers.csv'))
```

Use artifacts produced by your own training run and the same scikit-learn version recorded in its metrics. Joblib loading executes Python deserialization; load only trusted artifacts. The installed `telco_churn` package must be available.

## Operational interpretation

Risk thresholds are illustrative: Critical ≥50%, High ≥35%, Medium ≥20%, Low <20%. Validate thresholds, calibration, business costs, and a prospective prediction horizon before operational use. This historical dataset does not establish that the model works at customer signup.

`modeled_monthly_exposure` is the row's monthly charge multiplied by its model score. Sum rows to obtain portfolio exposure. It is distinct from the observed charges of customers who already churned. Do not infer causal retention effects from correlations.

Campaign scenarios accept explicit retention-lift and cost assumptions. They compare assumed first-month savings against one-time campaign costs. No guaranteed savings, intervention effectiveness, or measured ROI is claimed. Validate suggested offers through controlled experiments.

The Streamlit dashboard displays historical analysis; it does not perform model inference. Use the CLI or API above for scoring. See `docs/model_metrics.json` for the verified reference evaluation rather than relying on fixed risk-tier counts or historical example claims.
