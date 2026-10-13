# Team11 — SAND Reward Planner

A small Streamlit dashboard for a game studio's event operations lead to estimate how many SAND tokens a dollar-denominated rewards budget can fund.

## Step 1 — Dataset and decision-maker

**Dataset:** [Cryptocoins Historical Prices — CoinGecko on Kaggle](https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrency-historical-prices-coingecko), using only `the-sandbox.csv`.

| Item | Detail |
| --- | --- |
| Committed file | `data/the-sandbox.csv` |
| Size | 104,138 bytes, approximately 104 KB; no sampling required |
| Shape | 1,322 rows × 5 columns |
| Period | August 14, 2020–March 27, 2024 |
| Source | Historical market observations collected through the CoinGecko API; real market data |
| One row | One daily SAND observation; the dataset description specifies 00:00 sampling without explicitly naming a time zone |
| Fields | `date`, `price`, `total_volume`, `market_cap`, `coin_name` |
| Units | Price in USD per SAND; market capitalization and trading volume in USD |

The decision-maker is **a game studio's event operations lead**, responsible for setting token rewards within a fixed USD budget. This is a proposed business scenario: the dataset contains market observations, not a studio's actual campaign spending or revenue.

## Step 2 — Why this dashboard

The manager reviews the dashboard at **09:00 UTC each day** and approves the next campaign's reward allocation **weekly**. A fixed USD budget buys a different number of tokens as the reference price changes, so the same budgeting question recurs.

> If the event operations lead sees that SAND's reference price has changed by at least 10% in either direction over seven calendar days, they will review the planned token reward quantities before approving the next campaign.

The 10% threshold is an illustrative internal planning rule for this exercise. It is not a statistically optimized threshold or a trading recommendation.

Without the dashboard, the manager would look up a price, find the observation from seven days earlier, calculate the change, divide the campaign budget by the price, and copy the result into a planning sheet. That repeats several manual steps and risks mixing dates, units, or formulas. The expected cost is staff time and budgeting errors; we have not measured a specific time saving.

A dashboard keeps the reference price, budget calculation, and recent context together. A one-off report would become stale, while a weekly email would not let the manager change the budget or date range during planning. An alert can flag a threshold crossing, but the manager still needs the chart and budget estimate to review its effect. In production, an alert could complement this page.

## Step 3 — What matters, and what we cut

The Pandas and Matplotlib exploration is saved in [`notebooks/eda.ipynb`](notebooks/eda.ipynb). It checks shape, types, missing values, duplicate dates, daily coverage, distributions, and relationships before selecting the dashboard elements.

| EDA finding | Effect on the design |
| --- | --- |
| No missing values, duplicate rows, or duplicate dates; all 1,322 calendar dates are present | Keep the daily observations without imputation or aggregation |
| Price ranges from $0.03085 to $7.51364 across the snapshot | Use a recent 90-day default and a date control rather than making the full history the only view |
| Median reported volume at the daily observations is about $126 million; the maximum is about $8.71 billion | Show the volume trend to reveal spikes, while avoiding claims that volume guarantees liquidity |
| Price and market capitalization have a Pearson correlation of about 0.972 in this snapshot | Market capitalization adds little to the selected budgeting decision, supporting its exclusion |

### Three headline numbers

| KPI | Calculation and purpose |
| --- | --- |
| Reference price | Price on the last date in the selected range; the input to the reward budget calculation |
| 7-day price change | `(reference price / price seven calendar days earlier − 1) × 100`; shows whether the example review threshold is reached |
| Estimated reward pool (SAND) | `USD budget / reference price`; estimates the token quantity the entered budget can fund |

The seven-day comparison uses the full dataset, even when the visible date range is shorter than a week. If the exact comparison date is unavailable, the app displays **N/A**. The budget estimate uses the selected period's last observation and excludes fees and slippage; it is a planning scenario rather than an executed quote.

### Two charts and two controls

1. **Price trend:** the direct explanation for changes in the token quantity a fixed dollar budget can fund. The date range defaults to the last 90 days so recent movements remain readable.
2. **Trading-volume trend:** context for changes in market activity. High reported volume does not measure order-book depth or guarantee execution liquidity.

The only inputs are **a date range** and **a USD rewards budget**. The first supports comparing campaign periods; the second turns market prices into the manager's planning quantity. A single-token dataset does not need a coin selector.

### Two deliberate exclusions

1. **Market capitalization:** explored in the notebook, but it does not enter the reward budget calculation. Its three early zero values also require care. Adding another market-size chart would compete with the two questions the manager needs to answer.
2. **Price predictions, technical indicators, and return rankings:** the notebook explores historical changes, but those features would turn a campaign budgeting page into an investment tool and add assumptions the decision does not need.

### Data interpretation

Each row is a **daily reference observation**, not an OHLC candle or a daily closing price. The dashboard labels it accordingly. Its snapshot ends on **March 27, 2024**, so “reference price” always means the last selected historical observation, not today's market price. The data-period caption stays visible near the top of the page.

Three early `market_cap` observations are zero. We treat them as unavailable, not evidence that SAND had no value. Market capitalization is excluded from calculations; the expandable source table retains the original values and explains their interpretation.

### Page sketch and reading order

```text
Sidebar: [Date range] [USD rewards budget]

Team11: SAND Reward Planner
Who uses it and which reward-budget decision it supports
Historical data period · Intended production refresh

[Reference price] [7-day change] [Estimated reward pool]
Review status against the example 10% threshold

[Price trend — wider chart] [Trading-volume trend]

[Expandable source data and assumptions]
```

The top answers whether the reward plan needs review and what the budget funds. The middle supplies the market context, with more width given to the price chart because price directly determines the reward quantity. The optional table sits at the bottom so a manager can verify particular observations without adding a third main chart.

The visual design follows a restrained cyberpunk style: a dark navy background, cyan and violet chart accents, thin borders, and large metric values. The layout keeps the three KPIs prominent and avoids animation or decorative panels that would compete with the budgeting decision.

## Step 4 — Refresh and action

**Production refresh:** once daily, shortly after the 00:00 UTC reference observation is available. **Human review:** 09:00 UTC daily, with a weekly reward-allocation approval. Daily data makes a large change visible before the next campaign decision; minute-by-minute updates would add work without changing this weekly allocation process. This teaching app reads the committed historical CSV and does not fetch live prices.

Track the **seven-calendar-day price change** over time. At an absolute change of **10% or more**, the manager reviews the planned token quantities, checks the updated budget estimate, and confirms the next campaign's allocation before approval. A price increase reduces the SAND quantity a fixed USD budget funds; a decrease increases it. The rule prompts a review rather than an automatic purchase or sale.

A one-day delay can leave the manager using a reference price that has already moved. A week-old reference can misstate the planned token allocation at the approval point, causing an over-budget commitment or a reward quantity that no longer matches the intended dollar value. The visible data-period and refresh caption helps the manager judge whether the observation is suitable for a live decision.

## Run locally

The project was initialized with `uv init` and targets **Python 3.14**.

```bash
uv sync
uv run streamlit run app.py
```

To work on the EDA notebook, install the development dependencies with `uv sync --group dev` and select the project's `.venv` Python kernel in your notebook editor.

The CSV is included in the repository; no separate Kaggle download or API key is needed to run the app. Runtime dependencies are listed in the root [`requirements.txt`](requirements.txt). Streamlit Cloud prioritizes the committed `uv.lock` when both are present; it locks the same direct runtime package versions. See the [official dependency-file priority](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies).

Local validation passed six interaction checks covering budget arithmetic, single-day and partial date selections, the unavailable seven-day comparison, and rounding close to the review threshold. The EDA notebook includes its executed results and figures.

## Deploy to Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud and create an app from the public GitHub repository [`minaloushe-zia/sand-dashboard`](https://github.com/minaloushe-zia/sand-dashboard).
2. Select branch **`main`** and entrypoint **`app.py`**.
3. Under **Advanced settings**, choose **Python 3.14**, as required by the assignment.
4. Deploy, check that the page loads with the bundled CSV, then copy the resulting app URL.

The app title uses **Team11**; the team name can be edited in the constant near the top of `app.py`. For submission, provide the deployed app URL and the GitHub repository URL. Each student should follow the assignment's requirement to submit their own app and repository.
