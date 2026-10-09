import io
import json

import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from streamlit.testing.v1 import AppTest

from telco_churn import data
from telco_churn.__main__ import analyze
from telco_churn.data import CATEGORICAL, FEATURES, ROOT, clean_data
from telco_churn.model import make_pipeline, risk_tiers, scenario, score, train


@pytest.fixture
def customers():
    n = 100
    frame = pd.DataFrame({col: ["Yes", "No"] * (n // 2) for col in CATEGORICAL})
    frame["customerID"] = [f"id-{i}" for i in range(n)]
    frame["tenure"] = np.arange(n) % 72
    frame["MonthlyCharges"] = 20 + np.arange(n)
    frame["TotalCharges"] = frame.tenure * frame.MonthlyCharges
    frame["SeniorCitizen"] = np.arange(n) % 2
    frame["Contract"] = ["Month-to-month", "One year"] * (n // 2)
    frame["PaymentMethod"] = ["Electronic check", "Bank transfer (automatic)"] * (
        n // 2
    )
    frame["Churn"] = ["Yes", "No"] * (n // 2)
    return frame


def test_cleaning_and_target_validation(customers):
    customers.loc[0, "TotalCharges"] = np.nan
    customers.loc[0, "Contract"] = " Month-to-month "
    result = clean_data(customers)
    assert pd.isna(result.loc[0, "TotalCharges"])
    assert result.loc[0, "Contract"] == "Month-to-month"
    assert result.Churn.sum() == 50
    customers.loc[0, "Churn"] = "maybe"
    with pytest.raises(ValueError, match="Churn labels"):
        clean_data(customers)


@pytest.mark.parametrize("problem", ["missing", "negative", "duplicate", "invalid"])
def test_reject_bad_inputs(customers, problem):
    if problem == "missing":
        customers = customers.drop(columns="Contract")
    elif problem == "negative":
        customers.loc[0, "MonthlyCharges"] = -1
    elif problem == "duplicate":
        customers.loc[0, "customerID"] = customers.loc[1, "customerID"]
    else:
        customers["TotalCharges"] = customers.TotalCharges.astype(object)
        customers.loc[0, "TotalCharges"] = "not a number"
    with pytest.raises(ValueError):
        clean_data(customers)


def test_pipeline_roundtrip_and_unseen_categories(customers, tmp_path):
    df = clean_data(customers)
    pipeline = make_pipeline(LogisticRegression(max_iter=1000)).fit(
        df[FEATURES], df.Churn
    )
    path = tmp_path / "pipeline.joblib"
    joblib.dump(pipeline, path)
    future = customers.drop(columns="Churn").iloc[:3].copy()
    future.loc[0, "Contract"] = "New plan"
    future.loc[0, "TotalCharges"] = np.nan
    before = score(pipeline, future)
    after = score(joblib.load(path), future)
    np.testing.assert_allclose(before.churn_probability, after.churn_probability)
    assert after.churn_probability.between(0, 1).all()
    assert "Churn" not in after
    assert after.recommended_actions.notna().all()


def test_risk_boundaries():
    assert list(
        risk_tiers(np.array([0, 0.1999, 0.2, 0.3499, 0.35, 0.4999, 0.5, 1]))
    ) == ["Low", "Low", "Medium", "Medium", "High", "High", "Critical", "Critical"]


def test_weighted_exposure_and_scenario(customers):
    df = clean_data(customers)
    pipeline = make_pipeline(LogisticRegression(max_iter=1000)).fit(
        df[FEATURES], df.Churn
    )
    scores = score(pipeline, customers)
    expected = (scores.MonthlyCharges * scores.churn_probability).sum()
    result = scenario(scores, 0.25, 20)
    assert result["modeled_monthly_exposure"] == pytest.approx(expected)
    assert result["first_month_net"] == pytest.approx(expected * 0.25 - 2000)
    with pytest.raises(ValueError):
        scenario(scores, 1.1, 20)


def test_sql_matches_pandas(customers, tmp_path):
    df = clean_data(customers)
    analyze(df, tmp_path)
    snapshot = pd.read_csv(tmp_path / "00_exec_snapshot.csv").iloc[0]
    assert snapshot.customers == len(df)
    assert snapshot.churn_rate == df.Churn.mean()
    assert (
        snapshot.observed_churn_monthly_charges
        == df.loc[df.Churn.eq(1), "MonthlyCharges"].sum()
    )
    assert len(list(tmp_path.glob("*.csv"))) == 5


def test_download_validates_before_writing(customers, tmp_path, monkeypatch):
    monkeypatch.setattr(
        data,
        "urlopen",
        lambda *a, **k: io.BytesIO(customers.to_csv(index=False).encode()),
    )
    path = data.download_data(tmp_path / "data.csv")
    assert len(data.load_data(path)) == 100
    monkeypatch.setattr(data, "urlopen", lambda *a, **k: io.BytesIO(b"bad,data\n1,2\n"))
    with pytest.raises(ValueError):
        data.download_data(path)
    assert len(data.load_data(path)) == 100


def test_holdout_is_separate_and_metrics_serializable(customers):
    pipeline, metrics, holdout = train(customers)
    assert metrics["training_customers"] == 80
    assert metrics["test_customers"] == len(holdout) == 20
    assert len(metrics["candidates"]) == 3
    assert all(0 <= v <= 1 for v in metrics["holdout"].values())
    assert len(pipeline.named_steps["preprocessing"].feature_names_in_) == len(FEATURES)
    json.dumps(metrics)


def test_dashboard_filters(customers, monkeypatch):
    monkeypatch.setattr(data, "load_data", lambda: clean_data(customers))
    monkeypatch.setattr(data, "DATA_PATH", ROOT / "README.md")
    app = AppTest.from_file(str(ROOT / "dashboard/app.py")).run()
    assert not app.exception
    assert app.metric[0].value == "100"
    app.multiselect[0].set_value([]).run()
    assert not app.exception
    assert app.warning[0].value == "No rows match the selected filters."
