import streamlit as st

def render_sidebar(raw_df):
    st.sidebar.title("🏦 Filters")
    st.sidebar.caption("Segment the customer base. All KPIs and charts update live.")

    geo_options = sorted(raw_df["Geography"].dropna().unique().tolist())
    gender_options = sorted(raw_df["Gender"].dropna().unique().tolist())
    age_options = ["<30", "30-45", "46-60", "60+"]
    credit_options = ["Low", "Medium", "High"]
    tenure_options = ["New (0-2 yrs)", "Mid-term (3-6 yrs)", "Long-term (7+ yrs)"]
    balance_options = ["Zero-balance", "Low-balance", "High-balance"]

    sel_geo = st.sidebar.multiselect("Geography", geo_options, default=geo_options)
    sel_gender = st.sidebar.multiselect("Gender", gender_options, default=gender_options)
    sel_age = st.sidebar.multiselect("Age group", age_options, default=age_options)
    sel_credit = st.sidebar.multiselect("Credit score band", credit_options, default=credit_options)
    sel_tenure = st.sidebar.multiselect("Tenure group", tenure_options, default=tenure_options)
    sel_balance = st.sidebar.multiselect("Balance segment", balance_options, default=balance_options)

    active_only = st.sidebar.checkbox("Active members only", value=False)
    hv_only = st.sidebar.checkbox("High-value customers only (top 25% balance)", value=False)

    st.sidebar.markdown("---")
    if st.sidebar.button("Reset filters"):
        st.rerun()

    return {
        "geo": sel_geo,
        "gender": sel_gender,
        "age": sel_age,
        "credit": sel_credit,
        "tenure": sel_tenure,
        "balance": sel_balance,
        "active_only": active_only,
        "hv_only": hv_only,
    }

def apply_filters(raw_df, filters):
    df = raw_df[
        raw_df["Geography"].isin(filters["geo"])
        & raw_df["Gender"].isin(filters["gender"])
        & raw_df["AgeGroup"].astype(str).isin(filters["age"])
        & raw_df["CreditScoreBand"].astype(str).isin(filters["credit"])
        & raw_df["TenureGroup"].astype(str).isin(filters["tenure"])
        & raw_df["BalanceSegment"].isin(filters["balance"])
    ].copy()

    if filters["active_only"]:
        df = df[df["IsActiveMember"] == 1]

    if filters["hv_only"]:
        df = df[df["HighValue"]]

    return df
