"""Persist preprocessing and estimator together; keep test data untouched."""

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data import CATEGORICAL, FEATURES, NUMERIC, clean_data


def make_pipeline(estimator):
    preprocessing = ColumnTransformer(
        [
            (
                "numeric",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler()),
                    ]
                ),
                NUMERIC,
            ),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL,
            ),
        ]
    )
    return Pipeline([("preprocessing", preprocessing), ("model", estimator)])


def train(df):
    df = clean_data(df)
    x_train, x_test, y_train, y_test = train_test_split(
        df[FEATURES], df["Churn"], test_size=0.2, random_state=42, stratify=df["Churn"]
    )
    estimators = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=100, max_depth=3, random_state=42
        ),
    }
    candidates = []
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for name, estimator in estimators.items():
        pipeline = make_pipeline(estimator)
        scores = cross_val_score(pipeline, x_train, y_train, cv=cv, scoring="roc_auc")
        candidates.append(
            {
                "model": name,
                "cv_roc_auc_mean": float(scores.mean()),
                "cv_roc_auc_std": float(scores.std()),
            }
        )
    best = max(candidates, key=lambda row: row["cv_roc_auc_mean"])["model"]
    pipeline = make_pipeline(estimators[best]).fit(x_train, y_train)
    probability = pipeline.predict_proba(x_test)[:, 1]
    predicted = (probability >= 0.5).astype(int)
    metrics = {
        "best_model": best,
        "selection": "5-fold training-only cross-validation ROC AUC",
        "seed": 42,
        "training_customers": len(x_train),
        "test_customers": len(x_test),
        "candidates": candidates,
        "holdout": {
            "roc_auc": float(roc_auc_score(y_test, probability)),
            "accuracy": float(accuracy_score(y_test, predicted)),
            "precision": float(precision_score(y_test, predicted, zero_division=0)),
            "recall": float(recall_score(y_test, predicted, zero_division=0)),
            "f1": float(f1_score(y_test, predicted, zero_division=0)),
        },
    }
    holdout = df.loc[x_test.index].copy()
    holdout["churn_probability"] = probability
    return pipeline, metrics, holdout


def risk_tiers(probability):
    return np.select(
        [probability >= 0.5, probability >= 0.35, probability >= 0.2],
        ["Critical", "High", "Medium"],
        default="Low",
    )


def score(pipeline, df):
    df = clean_data(df, require_target=False)
    result = df.copy()
    result["churn_probability"] = pipeline.predict_proba(df[FEATURES])[:, 1]
    result["risk_tier"] = risk_tiers(result["churn_probability"])
    result["modeled_monthly_exposure"] = (
        result["MonthlyCharges"] * result["churn_probability"]
    )
    result["recommended_actions"] = result.apply(recommend, axis=1)
    return result.sort_values("churn_probability", ascending=False)


def recommend(row):
    actions = [
        {
            "Critical": "Review for proactive retention outreach",
            "High": "Review personalized retention offer",
            "Medium": "Satisfaction survey",
            "Low": "Standard engagement",
        }[row["risk_tier"]]
    ]
    if row["risk_tier"] in ("Critical", "High"):
        if row["tenure"] < 6:
            actions.append("Early onboarding check-in")
        if row["Contract"] == "Month-to-month":
            actions.append("Evaluate annual-plan incentive")
        if row["TechSupport"] == "No" and row["OnlineSecurity"] == "No":
            actions.append("Evaluate support bundle")
        if row["PaymentMethod"] == "Electronic check":
            actions.append("Offer auto-pay enrollment")
    return " | ".join(actions)


def scenario(scores, retention_lift, cost_per_customer):
    if not 0 <= retention_lift <= 1 or cost_per_customer < 0:
        raise ValueError("Lift must be between 0 and 1; cost must be nonnegative")
    exposure = float(scores["modeled_monthly_exposure"].sum())
    saved = exposure * retention_lift
    cost = len(scores) * cost_per_customer
    return {
        "modeled_monthly_exposure": exposure,
        "assumed_revenue_saved": saved,
        "campaign_cost": cost,
        "first_month_net": saved - cost,
    }
