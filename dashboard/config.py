import streamlit as st

DATA_PATH = "European_Bank.csv"

def configure_page():
    st.set_page_config(
        page_title="European Banking | Churn Analytics",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
