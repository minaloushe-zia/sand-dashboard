"""A small SAND reward-budget dashboard for Team11."""

from pathlib import Path

import pandas as pd
import streamlit as st


TEAM_NAME = "Team11"
DATA_PATH = Path(__file__).resolve().parent / "data" / "the-sandbox.csv"
REVIEW_THRESHOLD = 10.0

st.set_page_config(page_title=f"SAND Reward Planner | {TEAM_NAME}", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(ellipse at 90% 0%, rgba(123, 80, 255, .10), transparent 42%),
                    radial-gradient(ellipse at 15% 0%, rgba(38, 240, 229, .06), transparent 38%),
                    #080C15;
    }
    [data-testid="stMainBlockContainer"] {padding-top: 2.7rem; padding-bottom: 2rem; max-width: 1540px;}
    [data-testid="stSidebar"] {border-right: 1px solid rgba(38, 240, 229, .12);}
    h1 {letter-spacing: -.045em; font-weight: 750 !important; font-size: clamp(2rem, 3.1vw, 3rem) !important;}
    h2, h3 {letter-spacing: -.02em;}
    h3 {font-size: 1.15rem !important; font-weight: 600 !important;}
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(21, 30, 47, .95), rgba(12, 18, 31, .95));
        border: 1px solid rgba(132, 155, 193, .20);
        border-top: 2px solid rgba(38, 240, 229, .65);
        border-radius: 14px;
        padding: 20px 22px;
        min-height: 145px;
    }
    [data-testid="stMetricValue"] {
        color: #41F4E5;
        font-family: "Cascadia Code", "SFMono-Regular", Consolas, monospace;
        font-size: clamp(1.5rem, 2.3vw, 2.35rem);
        font-weight: 600;
    }
    [data-testid="stMetricLabel"] {color: #A8B7CD;}
    [data-testid="stVerticalBlockBorderWrapper"] > div {border-color: rgba(132, 155, 193, .15) !important;}
    [data-testid="stExpander"] {border: 1px solid rgba(132, 155, 193, .18); border-radius: 12px;}
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {color: #AAB8CC;}
    .dashboard-kicker {color: #41F4E5; font: 600 .75rem/1.6 Consolas, monospace; letter-spacing: .16em; margin: 0 0 8px;}
    .dashboard-rule {height: 1px; background: linear-gradient(90deg, #26F0E5, #9271FF 45%, transparent 95%); opacity: .55; margin: 20px 0 22px;}
    @media (max-width: 700px) {
        [data-testid="stMainBlockContainer"] {padding-top: 1.6rem;}
        [data-testid="stMetric"] {min-height: 110px; padding: 16px;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    """Read the committed Kaggle snapshot without making network requests."""
    data = pd.read_csv(DATA_PATH, parse_dates=["date"])
    data = data.sort_values("date").reset_index(drop=True)
    if data.empty or data["date"].isna().any():
        raise ValueError("The snapshot must contain valid observation dates.")
    if data["date"].duplicated().any():
        raise ValueError("The snapshot contains duplicate observation dates.")
    if data["price"].isna().any() or not data["price"].gt(0).all():
        raise ValueError("Reward calculations require a positive price on every date.")
    return data


st.markdown('<p class="dashboard-kicker">GAME ECONOMY / REWARD OPERATIONS</p>', unsafe_allow_html=True)
st.title(f"{TEAM_NAME}: SAND Reward Planner")
st.caption(
    "For a game studio's event operations lead to size SAND rewards "
    "within a fixed US-dollar budget."
)

try:
    data = load_data()
except (OSError, ValueError, KeyError) as error:
    st.error(f"Unable to load the SAND snapshot: {error}")
    st.stop()

first_date = data["date"].min().date()
last_date = data["date"].max().date()
st.caption(
    f"Data: {first_date:%d %b %Y} to {last_date:%d %b %Y}. Historical Kaggle snapshot. "
    "Proposed production refresh: daily after 00:00 UTC."
)
st.markdown('<div class="dashboard-rule"></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Plan an event")
    period = st.date_input(
        "Review period",
        value=(max(first_date, (pd.Timestamp(last_date) - pd.Timedelta(days=89)).date()), last_date),
        min_value=first_date,
        max_value=last_date,
        format="YYYY-MM-DD",
        key="review_period",
    )
    budget = st.number_input(
        "Reward budget (USD)",
        min_value=0.0,
        max_value=1_000_000_000.0,
        value=1_000.0,
        step=100.0,
        key="reward_budget",
        help="An illustrative event budget, before exchange fees and slippage.",
    )
    st.caption(
        "The reward estimate uses the last available price in your review period. "
        "The dates below refer to historical observations."
    )

if len(period) != 2:
    st.info("Select both a start date and an end date to review an event budget.")
    st.stop()

start_date, end_date = period
selected = data.loc[data["date"].between(pd.Timestamp(start_date), pd.Timestamp(end_date))]
if selected.empty:
    st.warning("There are no observations in this period. Choose another date range.")
    st.stop()

latest = selected.iloc[-1]
reference_date = latest["date"]
reference_price = float(latest["price"])
prior = data.loc[data["date"].eq(reference_date - pd.Timedelta(days=7)), "price"]
weekly_change = None if prior.empty else (reference_price / float(prior.iloc[0]) - 1) * 100
reward_quantity = budget / reference_price

price_column, change_column, reward_column = st.columns(3)
price_column.metric(
    "SAND reference price",
    f"${reference_price:,.4f}",
    help="CoinGecko's daily price observation in USD per SAND.",
)
change_column.metric(
    "7-day price change",
    "N/A" if weekly_change is None else f"{weekly_change:+.2f}%",
    help=(
        "Change from exactly seven calendar days before the reference date. "
        "The earlier observation may sit outside your selected review period."
    ),
)
reward_column.metric(
    "Estimated reward pool (SAND)",
    f"{reward_quantity:,.2f}",
    help="Your USD budget divided by the reference price, before fees and slippage.",
)
st.caption(
    f"Reference date: {reference_date:%d %b %Y}. "
    f"Scenario budget: ${budget:,.2f}. Quantities are estimates before fees and slippage."
)

if weekly_change is None:
    st.info("Seven days of prior price history are unavailable for this reference date.")
elif abs(weekly_change) >= REVIEW_THRESHOLD:
    st.warning(
        f"Budget review suggested: the 7-day price move is {weekly_change:+.2f}%. "
        "Recheck the token quantity before committing the next event's rewards."
    )
else:
    st.info("The 7-day price move is within the example 10% budget-review threshold.")
st.caption("Example operating rule: review the reward plan after a 7-day price move of 10% or more in either direction.")

price_chart, volume_chart = st.columns([2, 1])
with price_chart:
    st.subheader("SAND price")
    st.line_chart(
        selected.set_index("date")[["price"]].rename(columns={"price": "USD per SAND"}),
        x_label="Date",
        y_label="USD per SAND",
        color="#26F0E5",
        height=290,
        width="stretch",
    )
    st.caption("Daily price snapshots show how the dollar cost of token rewards changes.")

with volume_chart:
    st.subheader("Market trading activity")
    volume = selected.set_index("date")[["total_volume"]].div(1_000_000)
    st.bar_chart(
        volume.rename(columns={"total_volume": "USD millions"}),
        x_label="Date",
        y_label="USD millions",
        color="#A286FF",
        height=290,
        width="stretch",
    )
    st.caption("CoinGecko's reported market trading volume, shown in USD millions.")

with st.expander("Source data and assumptions"):
    st.markdown(
        "**Source:** [Kaggle: Cryptocoins Historical Prices — CoinGecko]"
        "(https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrency-historical-prices-coingecko). "
        "File: `the-sandbox.csv`. Prices are daily observations at 00:00 according to the "
        "dataset description, rather than daily closing or lowest prices.\n\n"
        "This reward budget is an illustrative planning scenario. Market trading volume "
        "measures activity across tracked markets; it does not measure this studio's revenue "
        "or the executable liquidity of a particular exchange. Three early market-cap values "
        "are zero and should be treated as unavailable. The snapshot does not update automatically."
    )
    st.dataframe(
        selected[["date", "price", "total_volume", "market_cap"]],
        hide_index=True,
        width="stretch",
        column_config={
            "date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "price": st.column_config.NumberColumn("Price (USD)", format="$%.4f"),
            "total_volume": st.column_config.NumberColumn("Trading volume (USD)", format="$%.0f"),
            "market_cap": st.column_config.NumberColumn("Market cap (USD)", format="$%.0f"),
        },
    )
