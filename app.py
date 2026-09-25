import streamlit as st

from dashboard.config import configure_page, DATA_PATH
from dashboard.data import load_data
from dashboard.filters import render_sidebar, apply_filters
from dashboard.metrics import render_kpis
from dashboard.tabs.overall import render_overall
from dashboard.tabs.geography import render_geography
from dashboard.tabs.age_tenure import render_age_tenure
from dashboard.tabs.high_value import render_high_value

configure_page()

try:
    raw_df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"Could not find `{DATA_PATH}`. Place the European_Bank.csv file "
        "in the same folder as this app, or upload it below."
    )
    uploaded = st.file_uploader("Upload European_Bank.csv", type="csv")
    if uploaded is not None:
        raw_df = load_data(uploaded)
    else:
        st.stop()

filters = render_sidebar(raw_df)
df = apply_filters(raw_df, filters)

if df.empty:
    st.warning("No customers match the selected filters. Adjust filters in the sidebar.")
    st.stop()

st.title("Customer Segmentation & Churn Pattern Analytics")
st.caption("European Banking · Interactive Analytics Dashboard")
st.markdown(f"**{len(df):,}** customers match current filters (of {len(raw_df):,} total).")

render_kpis(df, raw_df)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Overall Summary", "🌍 Geography", "👥 Age & Tenure", "💰 High-Value Explorer"]
)

with tab1:
    render_overall(df)

with tab2:
    render_geography(df)

with tab3:
    render_age_tenure(df)

with tab4:
    render_high_value(df)

st.markdown("---")
st.caption(
    "Customer Segmentation & Churn Pattern Analytics in European Banking · "
    "Dashboard generated with Streamlit & Plotly."
)
