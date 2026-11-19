"""FIN 439 Project 2: interactive portfolio stability dashboard."""

import hashlib
import io

import pandas as pd
import streamlit as st

from portfolio import (
    SLEEVES,
    CORRELATIONS,
    RESERVE_ELIGIBLE,
    search_lowest_risk,
    estimate_from_prices,
    benchmark_weights,
    covariance_matrix,
    equal_weights,
    expected_return,
    inverse_volatility_weights,
    portfolio_volatility,
)


st.set_page_config(
    page_title="Meridian Portfolio Dashboard",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7fb;
    }
    h1, h2, h3 {
        color: #132d46;
    }
    [data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #dce4ed;
        border-radius: 12px;
        padding: 18px;
    }
    [data-testid="stMetricValue"] {
        color: #132d46;
    }
    [data-testid="stSidebar"] {
        background-color: #eaf0f6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Meridian Portfolio Dashboard")
st.caption("Alyson Foster · FIN 439 · Project 2")
st.caption(
    "Built with ChatGPT assistance for code and presentation. "
    "The analysis and decision are mine. For education only. "
    "This is not investment advice."
)

with st.sidebar:
    st.header("Portfolio settings")

    objective = st.number_input(
        "Minimum annual return estimate (%)",
        value=6.5,
        step=0.1,
        format="%.2f",
    ) / 100

    reserve_min = st.number_input(
        "Minimum reserve-eligible weight (%)",
        min_value=0.0,
        max_value=100.0,
        value=3.0,
        step=1.0,
        format="%.2f",
    ) / 100

    upload = st.file_uploader(
        "Upload prices.csv",
        type=["csv"],
        help="The first column contains dates. Remaining columns contain prices.",
    )

    last_36 = st.checkbox("Use last 36 months", value=False)

    st.caption(
        "Upload the repository's prices.csv to reproduce the ETF results."
    )


def maximum_change(first, second):
