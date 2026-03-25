"""
Main Streamlit application for the dengue forecasting dashboard.

The landing page is intentionally lightweight: it orients the user, surfaces
the key checked-in artifacts, and routes them toward the forecasting or
cost-benefit pages where the deeper analysis lives.
"""
import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import src.config as config


st.set_page_config(
    page_title="Dengue Prevention Platform",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_landing_snapshot():
    """Load lightweight artifact summaries for the first screen."""
    snapshot = {}

    processed_path = config.PROCESSED_DATA_DIR / config.PROCESSED_DATA_FILE
    metrics_path = config.OUTPUT_DIR / f"{Path(config.MODEL_FILE).stem}_metrics.json"
    cba_path = config.OUTPUT_DIR / config.COST_BENEFIT_FILE

    if processed_path.exists():
        df = pd.read_csv(processed_path, parse_dates=[config.DATE_COLUMN])
        snapshot["records"] = len(df)
        snapshot["date_range"] = (
            f"{df[config.DATE_COLUMN].dt.year.min()}-{df[config.DATE_COLUMN].dt.year.max()}"
        )
        snapshot["cases_2020"] = int(
            df[df[config.DATE_COLUMN].dt.year == 2020][config.TARGET_VARIABLE].sum()
        )

    if metrics_path.exists():
        with open(metrics_path, "r", encoding="utf-8") as handle:
            snapshot["metrics"] = json.load(handle)

    if cba_path.exists():
        with open(cba_path, "r", encoding="utf-8") as handle:
            snapshot["cost_benefit"] = json.load(handle)

    return snapshot


st.title("🦟 Dengue Fever Forecasting & Analysis Platform")
st.markdown(
    """
    Forecast weekly dengue cases, then compare whether intervention spend changes the
    outbreak picture enough to justify the cost.

    Use the sidebar to open the forecasting or cost-benefit surface. This landing page
    gives the quickest snapshot of what is already packaged in the repo.
    """
)

snapshot = load_landing_snapshot()

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
with metric_col1:
    records = snapshot.get("records")
    st.metric("Weekly records", f"{records:,}" if records is not None else "N/A")
with metric_col2:
    st.metric("Coverage", snapshot.get("date_range", "N/A"))
with metric_col3:
    holdout_mape = snapshot.get("metrics", {}).get("holdout_mape")
    st.metric("Holdout MAPE", f"{holdout_mape:.1f}%" if holdout_mape is not None else "N/A")
with metric_col4:
    cases_2020 = snapshot.get("cases_2020")
    st.metric("2020 cases", f"{cases_2020:,}" if cases_2020 is not None else "N/A")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Forecast Explorer")
    st.markdown(
        """
        - Review the weekly dengue history and the current forecast horizon
        - Inspect confidence bands and recent predicted values
        - Use this page when the question is operational timing
        """
    )

with col2:
    st.markdown("### Cost-Benefit Analysis")
    st.markdown(
        """
        - Compare Wolbachia and Dengvaxia using DALYs, cost, and cases averted
        - Start here when the question is intervention tradeoffs, not only case counts
        - Use the scenario tab to test changes to efficacy and program assumptions
        """
    )

cost_benefit = snapshot.get("cost_benefit", {})
if cost_benefit:
    st.info(
        "Current checked-in analysis favors "
        f"**{cost_benefit.get('analysis_summary', {}).get('most_cost_effective_intervention', 'Wolbachia')}** "
        "as the more cost-effective intervention in the 2020 outbreak scenario."
    )
