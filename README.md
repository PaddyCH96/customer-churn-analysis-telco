# Telco Customer Churn and Revenue Exposure

A reproducible Python analytics case study using the IBM Telco Customer Churn dataset. SQL and an interactive Streamlit dashboard explain observed churn; a scikit-learn pipeline evaluates customer risk and suggests retention hypotheses.

## Verified dataset findings

The downloaded dataset contains **7,043 customers**, with **26.5% observed churn** and **$139,130.85 in monthly charges associated with customers labelled as churned**. This is historical exposure, not a forecast of future losses.

| Contract | Observed churn |
|---|---:|
| Month-to-month | 42.7% |
| One year | 11.3% |
| Two year | 2.8% |

Contract, tenure, payment method, and support availability are associated with churn. These observations do not prove that changing a contract or adding support causes retention improvements. Test retention offers through controlled campaigns.

## Run locally

Python 3.11–3.13 is tested in CI. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m telco_churn download
python -m telco_churn analyze
python -m telco_churn train
streamlit run dashboard/app.py
```

Download requires internet access. Once the CSV is available, analysis, training, notebooks, and the dashboard can run offline. The dashboard falls back to the same public IBM source when the local file is absent. To deploy on Streamlit Community Cloud, select `dashboard/app.py`; `requirements.txt` installs the local package and runtime dependencies.

## Modeling and measured evaluation

Preprocessing and the estimator are saved together in `reports/churn_pipeline.joblib`. Numeric missing values are imputed inside training folds, categorical values use one-hot encoding, and unseen categories are supported. Customer IDs and churn labels are excluded from features.

A stratified split reserves 20% of customers for final evaluation. Five-fold cross-validation on the remaining 80% selects among Logistic Regression, Random Forest, and Gradient Boosting. The holdout is not used for model selection.

The reference run selected **Gradient Boosting**. On **1,409 held-out customers**, it achieved:

| Metric | Value |
|---|---:|
| ROC AUC | 0.8434 |
| Accuracy | 80.6% |
| Precision | 67.4% |
| Recall | 52.4% |
| F1 | 0.5895 |

Classification metrics use a 0.5 threshold. [Reference metrics](docs/model_metrics.json) record the dataset SHA-256, package versions, seed, and cross-validation results. Rerun training to obtain results for your environment. The dataset is a historical snapshot without a prospective forecast horizon; probability calibration and business cutoff selection require further validation. These results do not establish signup-time performance or causal effects.

Risk tiers are Low (<20%), Medium (20–<35%), High (35–<50%), and Critical (≥50%). Full-dataset scoring includes training customers and must not be treated as holdout performance.

## Revenue definitions

- **Observed churn monthly charges:** sum of monthly charges for customers already labelled as churned, used by the SQL queries, EDA, and dashboard.
- **Modeled monthly exposure:** sum of each customer's monthly charge × predicted churn probability, used in scoring. It is an illustrative risk-weighted measure, not a calibrated future-loss forecast.
- **Campaign scenarios:** assumed retention lift × modeled exposure, minus assumed campaign cost. No retention lift, revenue savings, or ROI has been measured. Recommendations are hypotheses for review and experiments.

Tenure groups use explicit inclusive integer labels: 0–5, 6–11, 12–23, and 24+ months. The EDA further splits 24–47 and 48+.

## Repository layout

```text
src/telco_churn/     Shared validation, download, SQL analysis, training, and scoring
 dashboard/app.py   Streamlit dashboard (historical analysis)
 notebooks/         EDA and predictive workflow with executed outputs
 sql/               Five standalone DuckDB queries against a churn table
 tests/             Validation, SQL, inference, model, and dashboard checks
 docs/              Data, notebook, and reference evaluation documentation
 data/              Downloaded CSV (ignored by Git)
 reports/           Generated metrics, scores, SQL exports, and model (ignored)
 churn.duckdb       Legacy analysis snapshot; current workflow does not depend on it
 index.html         Redirect to the hosted Streamlit dashboard
```

For standalone SQL use a `churn` table with source Yes/No labels; the `analyze` command registers validated data automatically. Generated data and binary model files remain outside Git. Public, aggregate reference metrics are checked in under `docs/`.

## Checks and inference

```bash
ruff check src dashboard tests
black --check src dashboard tests
pytest --cov=telco_churn --cov-report=term-missing
python -m telco_churn score --data /path/to/customers.csv --model reports/churn_pipeline.joblib
```

Scoring accepts the original customer feature columns without `Churn`. See [deployment instructions](MODEL_DEPLOYMENT_GUIDE.md) and [notebook guide](docs/notebook_guide.md).

GitHub Actions checks Python 3.11, 3.12, and 3.13, runs tests, reproduces analysis/training, and uploads aggregate evaluation artifacts. It does not commit generated files.

## Author

Prudhvi Kadamuthuri
