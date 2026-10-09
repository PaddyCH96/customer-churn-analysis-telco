"""Dataset acquisition and validation shared by notebooks and dashboard."""

from pathlib import Path
from urllib.request import urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "telco_churn.csv"
DATA_URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
CATEGORICAL = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]
NUMERIC = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
FEATURES = NUMERIC + CATEGORICAL


def clean_data(df, require_target=True):
    df = df.copy()
    required = FEATURES + (["Churn"] if require_target else [])
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    for col in CATEGORICAL:
        df[col] = df[col].astype("string").str.strip().fillna("Unknown").astype(str)
    for col in NUMERIC:
        raw = df[col].replace(r"^\s*$", None, regex=True)
        converted = pd.to_numeric(raw, errors="coerce")
        if (raw.notna() & converted.isna()).any():
            raise ValueError(f"Invalid numeric values in {col}")
        if col != "TotalCharges" and converted.isna().any():
            raise ValueError(f"Missing values in {col}")
        if (converted.dropna() < 0).any():
            raise ValueError(f"Negative values in {col}")
        df[col] = converted
    if "Churn" in df:
        labels = df["Churn"].astype(str).str.strip().str.lower()
        mapped = labels.map({"yes": 1, "no": 0, "true": 1, "false": 0, "1": 1, "0": 0})
        if mapped.isna().any():
            raise ValueError("Invalid or missing Churn labels")
        df["Churn"] = mapped.astype(int)
    if "customerID" in df and (
        df["customerID"].isna().any() or df["customerID"].duplicated().any()
    ):
        raise ValueError("customerID must be present and unique")
    return df


def load_data(path=DATA_PATH):
    return clean_data(pd.read_csv(path))


def download_data(path=DATA_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(DATA_URL, timeout=60) as response:
        content = response.read()
    import io

    clean_data(pd.read_csv(io.BytesIO(content)))
    path.write_bytes(content)
    return path
