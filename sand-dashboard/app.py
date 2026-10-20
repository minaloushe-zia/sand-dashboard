"""A small SAND reward-budget dashboard for Team11."""

from pathlib import Path

import pandas as pd
import streamlit as st


TEAM_NAME = "Team11"
DATA_PATH = Path(__file__).resolve().parent / "data" / "the-sandbox.csv"
REVIEW_THRESHOLD = 10.0

st.set_page_config(
    page_title=f"SAND Reward Planner | {TEAM_NAME}",
    page_icon="💠",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --sand-ink: #070B14;
        --sand-text: #EDF4FF;
        --sand-muted: #A9B8CF;
        --sand-cyan: #31F5D5;
        --sand-purple: #B29AFF;
        --sand-line: rgba(149, 177, 217, .18);
    }
    .stApp {
        color: var(--sand-text);
        color-scheme: dark;
        background:
            radial-gradient(ellipse at 95% 5%, rgba(119, 65, 237, .12), transparent 36%),
            radial-gradient(ellipse at 0% 34%, rgba(0, 211, 195, .055), transparent 35%),
            var(--sand-ink);
    }
    [data-testid="stHeader"] {background: rgba(7, 11, 20, .92);}
    [data-testid="stToolbar"] {color: var(--sand-muted);}
    [data-testid="stMainBlockContainer"] {
        padding: 4.5rem 2.3rem 1.5rem;
        max-width: 1580px;
    }
    h1, h2, h3, h4 {color: var(--sand-text) !important;}
    h2, h3 {letter-spacing: -.025em;}
    h3 {font-size: 1.16rem !important; font-weight: 650 !important; padding-top: 0 !important;}
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stWidgetLabel"] p {color: #D5E0F0;}
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {
        color: var(--sand-muted) !important;
        font-size: .79rem;
        line-height: 1.7;
    }
    .command-bar {
        display: flex; justify-content: space-between; align-items: center;
        gap: 12px; margin: 0 0 17px;
        font: 600 .67rem/1.5 Consolas, monospace;
        letter-spacing: .13em; color: var(--sand-muted);
    }
    .command-name {color: var(--sand-cyan);}
    .snapshot-tag {
        display: inline-flex; align-items: center; gap: 8px;
        border: 1px solid rgba(255, 206, 100, .24); padding: 6px 10px;
        color: #FFD17A; background: rgba(255, 196, 73, .045);
    }
    .snapshot-tag::before {content: ""; width: 5px; height: 5px; background: #FFD17A;}
    .hero {
        position: relative; isolation: isolate; overflow: hidden;
        padding: 26px 30px 25px; margin-bottom: 6px;
        border: 1px solid rgba(49, 245, 213, .21);
        border-left: 3px solid var(--sand-cyan);
        background: linear-gradient(105deg, rgba(15, 30, 43, .97), rgba(19, 18, 43, .85));
    }
    .hero::before {
        content: ""; position: absolute; inset: 0; z-index: -1;
        background-image: linear-gradient(rgba(122, 177, 205, .045) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(122, 177, 205, .045) 1px, transparent 1px);
        background-size: 32px 32px;
        mask-image: linear-gradient(90deg, transparent 25%, #000);
    }
    .hero::after {
        content: ""; position: absolute; bottom: 0; right: 0;
        width: 90px; height: 3px; background: var(--sand-purple);
        box-shadow: 0 0 24px rgba(178, 154, 255, .6);
    }
    .hero-copy {position: relative; max-width: 76%; z-index: 1;}
    .hero-eyebrow {
        font: 600 .64rem/1.6 Consolas, monospace;
        letter-spacing: .17em; color: var(--sand-cyan); margin-bottom: 10px;
    }
    .hero h1 {
        margin: 0 !important; padding: 0 !important;
        font-size: clamp(2.1rem, 3.65vw, 3.65rem) !important;
        line-height: 1.04 !important; font-weight: 800 !important;
        letter-spacing: -.055em;
    }
    .hero h1 .hero-team {
        display: block; margin-bottom: 9px; color: #B5C5DB;
        font: 500 .7rem/1.4 Consolas, monospace; letter-spacing: .07em;
    }
    .hero-accent {color: var(--sand-cyan); text-shadow: 0 0 32px rgba(49, 245, 213, .18);}
    .hero-description {
        max-width: 620px; margin: 14px 0 0;
        font-size: .88rem; line-height: 1.65; color: #B7C8DC;
    }
    .hero-art {
        width: 178px; height: 178px; position: absolute; right: 25px; top: 50%;
        transform: translateY(-50%); opacity: .9; pointer-events: none;
        filter: drop-shadow(0 0 18px rgba(49, 245, 213, .13));
    }
    .hero-art::before, .hero-art::after {
        content: ""; position: absolute; border-radius: 50%;
    }
    .hero-art::before {inset: 0; border: 1px dashed rgba(178, 154, 255, .4);}
    .hero-art::after {
        inset: 15px; border: 1px solid rgba(49, 245, 213, .35);
        border-top: 3px solid var(--sand-cyan); border-bottom: 3px solid var(--sand-cyan);
        transform: rotate(-35deg);
    }
    .token-core {
        position: absolute; width: 89px; height: 89px; top: 44px; left: 44px;
        display: grid; place-items: center; transform: rotate(45deg);
        border: 1px solid rgba(49, 245, 213, .65);
        background: linear-gradient(140deg, rgba(49, 245, 213, .12), rgba(49, 245, 213, .025));
        box-shadow: inset 0 0 24px rgba(49, 245, 213, .06);
    }
    .token-core span {
        transform: rotate(-45deg); color: #74FFE5; font: 800 64px/1 Consolas, monospace;
        text-shadow: 0 0 22px rgba(49, 245, 213, .3);
    }
    .orbit-dot {
        position: absolute; right: 11px; top: 88px; width: 7px; height: 7px;
        background: var(--sand-purple); box-shadow: 0 0 12px rgba(178, 154, 255, .6);
    }
    .orbit-dot::after {
        content: ""; position: absolute; left: -150px; top: -2px;
        width: 5px; height: 5px; background: var(--sand-cyan);
    }
    .data-strip {
        margin: 3px 0 15px; padding: 12px 0;
        border-bottom: 1px solid var(--sand-line);
        display: flex; flex-wrap: wrap; column-gap: 22px; row-gap: 7px;
        color: #AFBFD4; font: .68rem/1.6 Consolas, monospace;
    }
    .data-strip strong {color: #E6EEFA; font-weight: 500;}
    [data-testid="stMetric"] {
        position: relative; overflow: hidden; min-height: 138px;
        padding: 23px 23px 19px; border: 1px solid var(--sand-line);
        border-top: 2px solid var(--sand-cyan); border-radius: 2px;
        background: linear-gradient(115deg, rgba(16, 33, 45, .95), rgba(12, 19, 33, .96));
        transition: border-color .2s, box-shadow .2s;
    }
    [data-testid="stMetric"]::after {
        content: ""; position: absolute; right: 11px; bottom: 9px;
        width: 7px; height: 7px;
        border-right: 1px solid rgba(49, 245, 213, .5);
        border-bottom: 1px solid rgba(49, 245, 213, .5);
    }
    [data-testid="stMetric"]:hover {
        border-color: rgba(49, 245, 213, .5);
        box-shadow: inset 0 0 30px rgba(49, 245, 213, .035), 0 0 22px rgba(49, 245, 213, .04);
    }
    [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] p {
        color: #B7C8DC !important; font-size: .79rem !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] p {
        color: #56FFE1 !important; font-family: "Cascadia Code", Consolas, monospace;
        font-size: clamp(1.7rem, 2.7vw, 2.7rem); font-weight: 600;
        letter-spacing: -.055em; line-height: 1.4;
        text-shadow: 0 0 25px rgba(49, 245, 213, .1);
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] {
        border-top-color: var(--sand-purple);
        background: linear-gradient(115deg, rgba(30, 25, 51, .95), rgba(14, 19, 34, .96));
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetricValue"],
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetricValue"] p {
        color: #C1ACFF !important;
    }
    [data-testid="stAlert"] {
        border-radius: 2px; border: 1px solid rgba(255, 209, 122, .2);
        border-left: 3px solid #FFD17A; background: rgba(255, 209, 122, .055);
    }
    [data-testid="stAlert"] p {color: #EDD6AB !important; font-size: .86rem;}
    .st-key-price_panel, .st-key-volume_panel {
        background: linear-gradient(145deg, rgba(15, 26, 42, .93), rgba(10, 16, 29, .97));
        border: 1px solid var(--sand-line) !important;
        border-radius: 3px !important; padding: 20px 20px 10px !important;
    }
    .panel-kicker {
        color: var(--sand-cyan); font: 500 .63rem/1.6 Consolas, monospace;
        letter-spacing: .13em; margin-bottom: 7px;
    }
    .panel-kicker.purple {color: var(--sand-purple);}
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1321, #080D17);
        border-right: 1px solid rgba(49, 245, 213, .18);
    }
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {padding-top: 1.5rem;}
    .sidebar-brand {
        display: flex; align-items: center; gap: 11px;
        color: var(--sand-text); font: 700 .95rem Consolas, monospace;
        letter-spacing: .07em; margin-bottom: 25px;
    }
    .sidebar-mark {font-size: 1.9rem; color: var(--sand-cyan); line-height: 1;}
    .sidebar-brand small {display: block; font-size: .57rem; color: #8DA4C1; margin-top: 6px; font-weight: 400;}
    .sidebar-label {
        padding-bottom: 10px; margin-bottom: 7px;
        border-bottom: 1px solid var(--sand-line);
        font: .63rem Consolas, monospace; letter-spacing: .13em; color: var(--sand-cyan);
    }
    [data-testid="stSidebar"] h2 {font-size: 1.3rem !important; padding-top: .2rem;}
    [data-testid="stSidebar"] input {color: #E6F0FF !important; background: #101D2E !important;}
    [data-testid="stNumberInput"] [data-baseweb="input"],
    [data-testid="stDateInput"] [data-baseweb="input"] {
        border: 1px solid rgba(109, 157, 196, .25); border-radius: 3px;
    }
    .sidebar-note {
        margin-top: 18px; padding: 13px 12px; border-left: 2px solid #7E69BE;
        background: rgba(178, 154, 255, .05); color: #A9B8CF;
        font-size: .73rem; line-height: 1.7;
    }
    .sidebar-note strong {color: #CCBAFF; font: .63rem Consolas, monospace; letter-spacing: .09em;}
    [data-testid="stExpander"] {
        border: 1px solid var(--sand-line); border-radius: 3px;
        background: rgba(11, 19, 32, .8);
    }
    [data-testid="stExpander"] summary {color: #B9C9DE;}
    .page-footer {
        display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap;
        border-top: 1px solid var(--sand-line); padding-top: 15px; margin-top: 18px;
        color: #879DBA; font: .59rem/1.7 Consolas, monospace; letter-spacing: .1em;
    }
    a:focus-visible, button:focus-visible, input:focus-visible, summary:focus-visible {
        outline: 2px solid var(--sand-cyan) !important; outline-offset: 3px;
    }
    @media (max-width: 1100px) {
        .hero-art {display: none;}
        .hero-copy {max-width: 100%;}
        [data-testid="stMetric"] {padding: 19px 16px;}
    }
    @media (max-width: 700px) {
        [data-testid="stMainBlockContainer"] {padding: 4.2rem 1.1rem 1.4rem;}
        .command-bar {font-size: .57rem; letter-spacing: .06em; align-items: flex-start;}
        .snapshot-tag {font-size: .52rem; padding: 4px 6px; white-space: nowrap;}
        .hero {padding: 23px 20px;}
        .hero-art {display: none;}
        .hero-copy {max-width: 100%;}
        .hero h1 {font-size: 2.35rem !important;}
        .hero-description {font-size: .79rem;}
        .hero-eyebrow {font-size: .57rem;}
        .data-strip {font-size: .61rem; gap: 6px;}
        .data-strip span {width: 100%;}
        [data-testid="stMetric"] {min-height: 115px; padding: 17px 19px;}
        [data-testid="stMetricValue"] {font-size: 2.05rem;}
        .st-key-price_panel, .st-key-volume_panel {padding: 16px 12px 8px !important;}
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {transition: none !important;}
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


st.html(
    f"""
    <div class="command-bar">
      <span class="command-name">◈ {TEAM_NAME.upper()} / GAME ECONOMY</span>
      <span class="snapshot-tag">HISTORICAL SNAPSHOT</span>
    </div>
    <section class="hero" aria-labelledby="dashboard-title">
      <div class="hero-copy">
        <div class="hero-eyebrow">REWARD OPERATIONS / THE SANDBOX</div>
        <h1 id="dashboard-title"><span class="hero-team">{TEAM_NAME}</span>
          <span class="hero-accent">SAND</span> REWARD<br>PLANNER<span class="hero-accent">.</span>
        </h1>
        <p class="hero-description">For a game studio's event operations lead to size SAND rewards
          within a fixed US-dollar budget.</p>
      </div>
      <div class="hero-art" aria-hidden="true">
        <div class="token-core"><span>S</span></div><i class="orbit-dot"></i>
      </div>
    </section>
    """
)

try:
    data = load_data()
except (OSError, ValueError, KeyError) as error:
    st.error(f"Unable to load the SAND snapshot: {error}")
    st.stop()

first_date = data["date"].min().date()
last_date = data["date"].max().date()
st.html(
    f'<div class="data-strip">'
    f'<span>DATA WINDOW / <strong>{first_date:%d %b %Y} — {last_date:%d %b %Y}</strong></span>'
    '<span>PROPOSED REFRESH / <strong>DAILY AFTER 00:00 UTC</strong></span>'
    '</div>'
)

with st.sidebar:
    st.html(
        '<div class="sidebar-brand"><span class="sidebar-mark">◈</span>'
        '<span>SAND LAB<small>TEAM11 / REWARD OPERATIONS</small></span></div>'
        '<div class="sidebar-label">01 / CONFIGURATION</div>'
    )
    st.header("Event controls")
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
    st.html(
        '<div class="sidebar-note"><strong>HISTORICAL MODE</strong><br>'
        'Explore a past campaign budget.<br>Changing the budget recalculates the '
        'estimated SAND allocation.</div>'
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
    with st.container(border=True, key="price_panel"):
        st.html('<div class="panel-kicker">01 / TOKEN VALUE</div>')
        st.subheader("SAND price")
        st.line_chart(
            selected.set_index("date")[["price"]].rename(columns={"price": "USD per SAND"}),
            x_label="Date",
            y_label="USD per SAND",
            color="#31F5D5",
            height=285,
            width="stretch",
        )
        st.caption("Daily price snapshots show how the dollar cost of token rewards changes.")

with volume_chart:
    with st.container(border=True, key="volume_panel"):
        st.html('<div class="panel-kicker purple">02 / MARKET ACTIVITY</div>')
        st.subheader("Trading volume")
        volume = selected.set_index("date")[["total_volume"]].div(1_000_000)
        st.bar_chart(
            volume.rename(columns={"total_volume": "USD millions"}),
            x_label="Date",
            y_label="USD millions",
            color="#B29AFF",
            height=285,
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

st.html(
    '<footer class="page-footer"><span>TEAM11 / SAND REWARD PLANNER</span>'
    '<span>KAGGLE · COINGECKO / HISTORICAL PLANNING SCENARIO</span></footer>'
)
