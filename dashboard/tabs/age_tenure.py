import streamlit as st
import plotly.express as px

def render_age_tenure(df):
    c1, c2 = st.columns([1, 1])

    with c1:
        age_summary = (
            df.groupby("AgeGroup", observed=True)["Exited"].mean().reset_index()
        )
        age_summary["Exited"] = age_summary["Exited"] * 100

        fig6 = px.bar(
            age_summary,
            x="AgeGroup",
            y="Exited",
            title="Churn Rate by Age Group",
            text=age_summary["Exited"].round(1).astype(str) + "%",
            color="Exited",
            color_continuous_scale="Blues",
        )
        fig6.update_layout(yaxis_title="Churn rate (%)")
        st.plotly_chart(fig6, width="stretch")

    with c2:
        tenure_summary = (
            df.groupby("TenureGroup", observed=True)["Exited"].mean().reset_index()
        )
        tenure_summary["Exited"] = tenure_summary["Exited"] * 100

        fig7 = px.bar(
            tenure_summary,
            x="TenureGroup",
            y="Exited",
            title="Churn Rate by Tenure Group",
            text=tenure_summary["Exited"].round(1).astype(str) + "%",
            color="Exited",
            color_continuous_scale="Purples",
        )
        fig7.update_layout(yaxis_title="Churn rate (%)")
        st.plotly_chart(fig7, width="stretch")

    st.markdown("#### Age x Tenure Heatmap")
    heat = (
        df.groupby(["AgeGroup", "TenureGroup"], observed=True)["Exited"]
        .mean()
        .reset_index()
    )
    heat["Exited"] = heat["Exited"] * 100
    heat_pivot = heat.pivot(index="AgeGroup", columns="TenureGroup", values="Exited")

    fig8 = px.imshow(
        heat_pivot,
        text_auto=".1f",
        color_continuous_scale="OrRd",
        aspect="auto",
        title="Churn Rate (%) — Age Group vs. Tenure Group",
    )
    st.plotly_chart(fig8, width="stretch")

    st.markdown("#### Engagement (Active vs. Inactive) vs. Churn")
    eng = df.groupby("ActiveLabel")["Exited"].mean().reset_index()
    eng["Exited"] = eng["Exited"] * 100

    fig9 = px.bar(
        eng,
        x="ActiveLabel",
        y="Exited",
        color="ActiveLabel",
        title="Churn Rate: Active vs. Inactive Members",
        text=eng["Exited"].round(1).astype(str) + "%",
        color_discrete_map={"Active": "#2E7D32", "Inactive": "#C62828"},
    )
    fig9.update_layout(yaxis_title="Churn rate (%)", showlegend=False)
    st.plotly_chart(fig9, width="stretch")
