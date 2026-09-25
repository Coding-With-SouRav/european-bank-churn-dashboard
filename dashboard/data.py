import numpy as np
import pandas as pd
import streamlit as st

@st.cache_data
def load_data(path) -> pd.DataFrame:
    df = pd.read_csv(path)

    binary_cols = ["HasCrCard", "IsActiveMember", "Exited"]
    for col in binary_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df["Balance"] = pd.to_numeric(df["Balance"], errors="coerce").fillna(0)
    df["EstimatedSalary"] = pd.to_numeric(df["EstimatedSalary"], errors="coerce").fillna(0)
    df["CreditScore"] = pd.to_numeric(df["CreditScore"], errors="coerce")
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Tenure"] = pd.to_numeric(df["Tenure"], errors="coerce")

    df = df.drop(columns=["Surname"], errors="ignore")
    df = df.dropna(subset=["CustomerId"])

    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 30, 45, 60, np.inf],
        labels=["<30", "30-45", "46-60", "60+"],
        right=True,
    )

    df["CreditScoreBand"] = pd.cut(
        df["CreditScore"],
        bins=[-np.inf, 579, 699, np.inf],
        labels=["Low", "Medium", "High"],
    )

    df["TenureGroup"] = pd.cut(
        df["Tenure"],
        bins=[-1, 2, 6, np.inf],
        labels=["New (0-2 yrs)", "Mid-term (3-6 yrs)", "Long-term (7+ yrs)"],
    )

    positive_balances = df.loc[df["Balance"] > 0, "Balance"]
    positive_median = positive_balances.median() if not positive_balances.empty else 0

    df["BalanceSegment"] = np.where(
        df["Balance"] <= 0,
        "Zero-balance",
        np.where(df["Balance"] < positive_median, "Low-balance", "High-balance"),
    )

    df["ChurnLabel"] = df["Exited"].map({0: "Retained", 1: "Churned"})
    df["ActiveLabel"] = df["IsActiveMember"].map({0: "Inactive", 1: "Active"})

    if (df["Balance"] > 0).any():
        hv_threshold = df.loc[df["Balance"] > 0, "Balance"].quantile(0.75)
    else:
        hv_threshold = 0

    df["HighValue"] = df["Balance"] >= hv_threshold

    return df
