import duckdb
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Telco Churn Dashboard", layout="wide")

@st.cache_data
def load_df():
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    con = duckdb.connect(database=":memory:")

    df = con.execute(f"""
        SELECT
          *,
          TRY_CAST(NULLIF(TotalCharges, ' ') AS DOUBLE) AS TotalCharges_num
        FROM read_csv_auto('{url}', HEADER=TRUE)
    """).df()

    # Normalize churn into a boolean column
    s = df["Churn"]
    if s.dtype == bool:
        df["churned"] = s
    else:
        df["churned"] = (
            s.astype(str).str.strip().str.lower().isin(["yes", "true", "1"])
        )

    # Clean whitespace in categoricals
    for col in ["Contract", "PaymentMethod", "InternetService", "TechSupport", "OnlineSecurity"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df

df = load_df()

st.title("Customer Churn & Revenue Risk Dashboard")
st.caption("Business-first view of churn drivers and monthly revenue at risk (IBM Telco dataset).")

# ---------------- Sidebar filters ----------------
st.sidebar.header("Filters")

contract_opts = sorted(df["Contract"].dropna().unique().tolist())
payment_opts = sorted(df["PaymentMethod"].dropna().unique().tolist())
internet_opts = sorted(df["InternetService"].dropna().unique().tolist())

contract = st.sidebar.multiselect("Contract", contract_opts, default=contract_opts)
payment = st.sidebar.multiselect("Payment Method", payment_opts, default=payment_opts)
internet = st.sidebar.multiselect("Internet Service", internet_opts, default=internet_opts)

tenure_max = int(df["tenure"].max())
tenure_range = st.sidebar.slider("Tenure (months)", 0, tenure_max, (0, tenure_max))

f = df[
    df["Contract"].isin(contract)
    & df["PaymentMethod"].isin(payment)
    & df["InternetService"].isin(internet)
    & df["tenure"].between(tenure_range[0], tenure_range[1])
].copy()

if f.empty:
    st.warning("No rows match the selected filters.")
    st.stop()

# ---------------- KPIs ----------------
customers = len(f)
churned = int(f["churned"].sum())
churn_rate = churned / customers
avg_monthly = float(f["MonthlyCharges"].mean())
rev_at_risk = float(f.loc[f["churned"], "MonthlyCharges"].sum())

k1, k2, k3, k4 = st.columns(4)
k1.metric("Customers", f"{customers:,}")
k2.metric("Churn rate", f"{churn_rate*100:.1f}%")
k3.metric("Churned customers", f"{churned:,}")
k4.metric("Monthly revenue at risk", f"${rev_at_risk:,.0f}")

st.divider()

# ---------------- Tabs ----------------
tab1, tab2, tab3 = st.tabs(["Drivers", "Tenure", "Revenue risk"])

with tab1:
    st.subheader("Churn drivers")

    by_contract = (
        f.groupby("Contract", as_index=False)
         .agg(customers=("customerID", "count"), churn_rate=("churned", "mean"))
         .sort_values("churn_rate", ascending=False)
    )

    fig = px.bar(
        by_contract,
        x="Contract",
        y="churn_rate",
        text=by_contract["churn_rate"].map(lambda x: f"{x*100:.1f}%"),
        hover_data={"customers": True, "churn_rate": ":.3f"},
        labels={"churn_rate": "Churn rate"},
        title="Churn rate by contract"
    )
    fig.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

    by_payment = (
        f.groupby("PaymentMethod", as_index=False)
         .agg(customers=("customerID", "count"), churn_rate=("churned", "mean"))
         .sort_values("churn_rate", ascending=False)
    )

    fig = px.bar(
        by_payment,
        x="PaymentMethod",
        y="churn_rate",
        text=by_payment["churn_rate"].map(lambda x: f"{x*100:.1f}%"),
        hover_data={"customers": True, "churn_rate": ":.3f"},
        labels={"churn_rate": "Churn rate"},
        title="Churn rate by payment method"
    )
    fig.update_layout(xaxis_tickangle=-20, yaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Churn over customer tenure")

    def bucket(t):
        if t < 6:
            return "0–6"
        if t < 12:
            return "6–12"
        if t < 24:
            return "12–24"
        return "24+"

    f["tenure_bucket"] = f["tenure"].apply(bucket)

    order = ["0–6", "6–12", "12–24", "24+"]
    by_tenure = (
        f.groupby("tenure_bucket", as_index=False)
         .agg(customers=("customerID", "count"), churn_rate=("churned", "mean"))
    )
    by_tenure["tenure_bucket"] = pd.Categorical(by_tenure["tenure_bucket"], categories=order, ordered=True)
    by_tenure = by_tenure.sort_values("tenure_bucket")

    fig = px.line(
        by_tenure,
        x="tenure_bucket",
        y="churn_rate",
        markers=True,
        hover_data={"customers": True, "churn_rate": ":.3f"},
        labels={"tenure_bucket": "Tenure bucket (months)", "churn_rate": "Churn rate"},
        title="Churn rate by tenure bucket"
    )
    fig.update_layout(yaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Where revenue risk concentrates")

    f["risk"] = f["MonthlyCharges"].where(f["churned"], 0.0)

    by_contract_risk = (
        f.groupby("Contract", as_index=False)
         .agg(customers=("customerID", "count"),
              churned=("churned", "sum"),
              revenue_at_risk=("risk", "sum"),
              churn_rate=("churned", "mean"))
         .sort_values("revenue_at_risk", ascending=False)
    )

    fig = px.bar(
        by_contract_risk,
        x="Contract",
        y="revenue_at_risk",
        hover_data={"customers": True, "churned": True, "churn_rate": ":.3f", "revenue_at_risk": ":.2f"},
        labels={"revenue_at_risk": "Monthly revenue at risk ($)"},
        title="Monthly revenue at risk by contract"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top churn-risk segments")

    seg = (
        f.groupby(["Contract", "PaymentMethod"], as_index=False)
         .agg(customers=("customerID", "count"),
              churn_rate=("churned", "mean"),
              revenue_at_risk=("risk", "sum"))
    )

    seg = seg[seg["customers"] >= 200].sort_values(
        ["churn_rate", "revenue_at_risk"], ascending=False
    ).head(10)

    seg["churn_rate"] = seg["churn_rate"].map(lambda x: f"{x*100:.1f}%")
    seg["revenue_at_risk"] = seg["revenue_at_risk"].map(lambda x: f"${x:,.0f}")

    st.dataframe(seg, use_container_width=True)

st.divider()

with st.expander("Show filtered data (sample)"):
    st.dataframe(f.head(50), use_container_width=True)

