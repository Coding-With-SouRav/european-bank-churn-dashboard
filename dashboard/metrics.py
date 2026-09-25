import streamlit as st

def churn_rate(frame):
    return frame["Exited"].mean() * 100 if len(frame) else 0.0

def render_kpis(df, raw_df):
    overall_rate = churn_rate(df)
    baseline_rate = churn_rate(raw_df)

    hv_rate = churn_rate(df[df["HighValue"]])
    geo_rates = df.groupby("Geography")["Exited"].mean() * 100
    geo_risk_idx = (geo_rates.max() - geo_rates.min()) if len(geo_rates) > 1 else 0.0

    inactive_churn = churn_rate(df[df["IsActiveMember"] == 0])
    active_churn = churn_rate(df[df["IsActiveMember"] == 1])
    engagement_drop = inactive_churn - active_churn

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric(
        "Overall Churn Rate",
        f"{overall_rate:.1f}%",
        f"{overall_rate - baseline_rate:+.1f} pp vs. all customers",
    )
    k2.metric("High-Value Churn Ratio", f"{hv_rate:.1f}%")
    k3.metric(
        "Geographic Risk Index",
        f"{geo_risk_idx:.1f} pp",
        "spread between highest & lowest region",
    )
    k4.metric(
        "Engagement Drop Indicator",
        f"{engagement_drop:.1f} pp",
        "inactive vs. active churn gap",
    )
    k5.metric("Active Member Share", f"{df['IsActiveMember'].mean()*100:.1f}%")
