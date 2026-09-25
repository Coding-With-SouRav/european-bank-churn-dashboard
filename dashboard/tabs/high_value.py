import streamlit as st
import plotly.express as px

from dashboard.metrics import churn_rate

def render_high_value(df):
    st.markdown(
        "High-value customers are defined as the **top 25% by account balance** "
        "(among customers holding a non-zero balance)."
    )

    hv_df = df[df["HighValue"]]

    c1, c2, c3 = st.columns(3)
    c1.metric("High-Value Customers", f"{len(hv_df):,}")
    c2.metric("High-Value Churn Rate", f"{churn_rate(hv_df):.1f}%")

    revenue_at_risk = hv_df.loc[hv_df["Exited"] == 1, "Balance"].sum()
    c3.metric("Balance at Risk (Churned HV)", f"€{revenue_at_risk:,.0f}")

    c1, c2 = st.columns([1, 1])

    with c1:
        fig10 = px.scatter(
            df,
            x="Balance",
            y="EstimatedSalary",
            color="ChurnLabel",
            symbol="HighValue",
            opacity=0.6,
            title="Balance vs. Estimated Salary (Churn Highlighted)",
            color_discrete_map={"Retained": "#2E7D32", "Churned": "#C62828"},
        )
        st.plotly_chart(fig10, width="stretch")

    with c2:
        hv_geo = hv_df.groupby("Geography")["Exited"].mean().reset_index()
        hv_geo["Exited"] = hv_geo["Exited"] * 100

        fig11 = px.bar(
            hv_geo.sort_values("Exited", ascending=False),
            x="Geography",
            y="Exited",
            title="High-Value Churn Rate by Country",
            text=hv_geo["Exited"].round(1).astype(str) + "%",
            color="Geography",
        )
        fig11.update_layout(yaxis_title="Churn rate (%)", showlegend=False)
        st.plotly_chart(fig11, width="stretch")

    st.markdown("#### Drill-down: High-Value Churned Customers")
    drill = hv_df[hv_df["Exited"] == 1][
        [
            "CustomerId",
            "Geography",
            "Gender",
            "Age",
            "Tenure",
            "Balance",
            "NumOfProducts",
            "CreditScore",
            "EstimatedSalary",
            "IsActiveMember",
        ]
    ].sort_values("Balance", ascending=False)

    st.dataframe(drill, width="stretch", hide_index=True)
    st.caption(f"{len(drill):,} high-value customers churned under current filters.")

    csv_download = drill.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download this table as CSV",
        data=csv_download,
        file_name="high_value_churned_customers.csv",
        mime="text/csv",
    )
