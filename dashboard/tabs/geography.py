import streamlit as st
import plotly.express as px

def render_geography(df):
    c1, c2 = st.columns([1, 1])

    with c1:
        geo_summary = (
            df.groupby("Geography")
            .agg(Customers=("CustomerId", "count"), ChurnRate=("Exited", "mean"))
            .reset_index()
        )
        geo_summary["ChurnRate"] = geo_summary["ChurnRate"] * 100

        fig3 = px.bar(
            geo_summary.sort_values("ChurnRate", ascending=False),
            x="Geography",
            y="ChurnRate",
            color="Geography",
            text=geo_summary["ChurnRate"].round(1).astype(str) + "%",
            title="Churn Rate by Country",
        )
        fig3.update_layout(yaxis_title="Churn rate (%)", showlegend=False)
        st.plotly_chart(fig3, width="stretch")

    with c2:
        fig4 = px.treemap(
            df,
            path=["Geography", "ChurnLabel"],
            title="Customer Volume: Country → Churn Status",
            color="Geography",
        )
        st.plotly_chart(fig4, width="stretch")

    st.markdown("#### Country x Gender Churn Interaction")
    geo_gender = df.groupby(["Geography", "Gender"])["Exited"].mean().reset_index()
    geo_gender["Exited"] = geo_gender["Exited"] * 100

    fig5 = px.bar(
        geo_gender,
        x="Geography",
        y="Exited",
        color="Gender",
        barmode="group",
        title="Churn Rate by Country and Gender",
        labels={"Exited": "Churn rate (%)"},
    )
    st.plotly_chart(fig5, width="stretch")

    st.dataframe(
        geo_summary.rename(columns={"ChurnRate": "Churn Rate (%)"}).round(1),
        width="stretch",
        hide_index=True,
    )
