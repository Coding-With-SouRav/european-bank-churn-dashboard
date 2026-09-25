import streamlit as st
import plotly.express as px

def render_overall(df):
    c1, c2 = st.columns([1, 1])

    with c1:
        churn_counts = df["ChurnLabel"].value_counts().reset_index()
        churn_counts.columns = ["Status", "Customers"]

        fig = px.pie(
            churn_counts,
            names="Status",
            values="Customers",
            hole=0.55,
            color="Status",
            color_discrete_map={"Retained": "#2E7D32", "Churned": "#C62828"},
            title="Retained vs. Churned Customers",
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, width="stretch")

    with c2:
        seg_choice = st.selectbox(
            "Compare churn rate by segment",
            [
                "Geography",
                "Gender",
                "AgeGroup",
                "CreditScoreBand",
                "TenureGroup",
                "BalanceSegment",
            ],
            index=0,
        )

        seg_rate = (
            df.groupby(seg_choice, observed=True)["Exited"]
            .agg(["mean", "count"])
            .reset_index()
        )
        seg_rate["mean"] = seg_rate["mean"] * 100
        seg_rate.columns = [seg_choice, "ChurnRate", "Customers"]
        seg_rate = seg_rate.sort_values("ChurnRate", ascending=False)

        fig2 = px.bar(
            seg_rate,
            x=seg_choice,
            y="ChurnRate",
            text=seg_rate["ChurnRate"].round(1).astype(str) + "%",
            title=f"Churn Rate by {seg_choice}",
            color="ChurnRate",
            color_continuous_scale="Reds",
        )
        fig2.update_layout(yaxis_title="Churn rate (%)")
        st.plotly_chart(fig2, width="stretch")

    st.markdown("#### Churned vs. Retained Profile Comparison")
    profile_cols = [
        "CreditScore",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "EstimatedSalary",
    ]
    profile = df.groupby("ChurnLabel")[profile_cols].mean().round(1).T
    st.dataframe(profile, width="stretch")
