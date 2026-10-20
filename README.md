# Team11 — SAND Reward Planner

I designed this dashboard for a game studio's event operations lead who needs to set SAND token rewards within a fixed US-dollar budget. My main design decision was to make the budget calculation the focus of the page, with enough price context to decide when the planned reward quantity needs review.

**Live app:** [SAND Reward Planner](https://sand-dashboard-myhhguoscjpbwpnfwffal2.streamlit.app/)  
**Repository:** [minaloushe-zia/sand-dashboard](https://github.com/minaloushe-zia/sand-dashboard)

## Step 1 — Dataset and decision-maker

I chose [Cryptocoins Historical Prices — CoinGecko on Kaggle](https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrency-historical-prices-coingecko) and used its `the-sandbox.csv` file. SAND connects the market data to a specific business problem: a game studio promising token rewards needs to understand how many tokens its dollar budget can fund.

| Dataset detail | What I used |
| --- | --- |
| Committed CSV | `sand-dashboard/data/the-sandbox.csv` |
| Size and shape | 104,138 bytes, approximately 104 KB; 1,322 rows and 5 columns |
| Period | August 14, 2020–March 27, 2024 |
| Source and type | Real market observations collected through CoinGecko and shared on Kaggle |
| One row | One daily SAND observation |
| Fields and units | Date, price in USD per SAND, reported trading volume in USD, market capitalization in USD, and coin name |

The file is well below 25 MB, so I kept the complete CSV without sampling. The dataset description specifies observations at 00:00 but does not explicitly identify a time zone. I therefore describe the prices as daily reference observations rather than daily closing prices.

My decision-maker is one role: **the game studio's event operations lead**. This person sets the token quantity for the next campaign and checks that the planned rewards remain affordable. The studio scenario is a proposed use of the market data; the CSV contains no actual studio campaign spending or revenue.

## Step 2 — Why this decision needs a dashboard

The lead would review the page at **09:00 UTC each day**, then approve the next campaign's reward allocation **weekly**. The recurring question is: how many SAND tokens can the current dollar budget fund, and has the price moved enough to reconsider the existing plan?

> If the event operations lead sees a SAND reference-price change of at least 10% in either direction over seven calendar days, they will review the planned token quantity before approving the next campaign's rewards.

I chose 10% as an example planning rule that prompts a deliberate budget check. It is a proposed operating threshold, rather than a threshold estimated from campaign outcomes.

Without the dashboard, the lead would look up a reference price, find the observation from seven days earlier, calculate the percentage change, and divide the dollar budget by the price in a spreadsheet. Repeating those steps costs staff time and creates opportunities to mix dates or use an outdated price. For example, if a fixed token allocation originally cost USD 1,000, a 10% price increase would raise its cost to USD 1,100 before fees. This illustrates the budgeting mistake the dashboard is intended to help prevent.

A dashboard suits this repeated, adjustable calculation. A report can explain a past campaign, but its budget estimate becomes stale as the reference price changes. A weekly email cannot let the lead change the budget or review period during planning. An alert can flag the 10% threshold, but the lead still needs the budget estimate and price trend to decide what to change. I therefore put the calculation and its supporting context on one page.

## Step 3 — What I showed, what I cut, and why

My [Pandas and Matplotlib EDA notebook](https://github.com/minaloushe-zia/sand-dashboard/blob/main/sand-dashboard/notebooks/eda.ipynb) checks shape, data types, missing values, duplicate dates, distributions, and relationships. I used these findings to choose the page contents:

| EDA finding | Design decision |
| --- | --- |
| All 1,322 dates are present, with no missing values or duplicate dates | Keep the daily observations without imputation or aggregation |
| Price ranges from USD 0.03085 to USD 7.51364 | Default to the last 90 days and allow a date filter, so the full historical range does not hide recent changes |
| Median reported volume is about USD 126 million and the maximum is about USD 8.71 billion | Keep a volume trend for market-activity context and retain the observed spikes |
| Price and market capitalization have a correlation of about 0.972 | Give the limited chart space to price and volume; market capitalization adds little to this budget calculation |

### Three headline metrics

| Metric | Why the lead needs it |
| --- | --- |
| SAND reference price | The price on the last date of the selected period is the input to the budget calculation |
| Seven-day price change | Shows whether the example 10% review threshold has been reached |
| Estimated reward pool in SAND | Converts the entered USD budget into the token quantity it can fund: `budget / reference price` |

For example, the snapshot's last reference price is approximately USD 0.720176 per SAND, so a USD 1,000 budget funds approximately 1,388.55 SAND before fees and slippage. That token quantity is the operational answer I want the lead to find first.

The seven-day change compares the reference observation with the observation exactly seven calendar days earlier, even if that earlier date is outside the visible range. If the comparison is unavailable, the page shows **N/A**. This avoids presenting a shorter interval as a seven-day change.

### Two charts and two inputs

I made the **price trend** the wider chart because it explains changes in the reward quantity a fixed dollar budget can fund. The **reported trading-volume trend** is a smaller supporting chart: it helps the lead see whether a price move coincides with a change in market activity. Volume is context; it does not establish the liquidity available for a particular purchase.

The only inputs are a **review date range** and a **USD reward budget**. The first lets the lead examine a campaign period; the second updates the proposed token allocation. I left out a coin selector because this decision concerns SAND alone.

### Two deliberate exclusions

1. **Market capitalization.** Its strong relationship with price makes it an interesting EDA result, but it does not enter the reward calculation or change the proposed review action. Three early market-cap observations are also zero. I excluded it from the headline metrics and charts, while retaining the source values in the optional data table.
2. **Price forecasts and technical trading indicators.** A campaign budget needs a reference price and a review rule. Forecasts, buy/sell signals, and return rankings would introduce additional assumptions and compete with that planning task, so I excluded them.

### Interpretation and reading order

The snapshot ends on **March 27, 2024**. I show the data period and a historical-snapshot label near the title, so the viewer can distinguish a past planning scenario from a current market quote. The expandable assumptions explain the daily observation convention, the three unavailable market-cap values, and the exclusion of fees and slippage. They also distinguish reported market volume from the studio's revenue and from executable exchange liquidity.

My page layout follows the order of the decision:

```text
Sidebar: [Review period] [USD reward budget]

Team11 — SAND Reward Planner
Decision-maker and purpose
Historical data period and intended refresh

[Reference price] [Seven-day change] [Estimated reward pool]
Review message against the 10% threshold

[Price trend — wider] [Trading-volume trend]

[Expandable source data and assumptions]
```

The top gives the budget answer and review status. The middle explains the price and activity behind it. The bottom lets the lead check particular observations without making the detailed table part of the main reading path. 

## Step 4 — Refresh frequency, review frequency, and action

For a production version, I would refresh the reference data **once daily, shortly after 00:00 UTC**, and have the lead review it at **09:00 UTC daily**. The weekly campaign approval is the main decision point; the daily check gives the lead time to revise a plan before approval. Minute-by-minute updates would add monitoring work without changing this allocation process. The current app reads the fixed historical CSV, so its stated refresh frequency is the proposed production schedule.

I would track the **absolute seven-calendar-day price change**. At **10% or more**, the lead should recalculate the token pool, check the campaign's reward commitments, and approve an adjusted quantity before committing the budget. A price rise reduces the quantity a fixed USD budget can fund; a fall increases it. The threshold triggers a human review.

A one-day-old price can leave the daily calculation behind the market and delay a budget check. A week-old price can carry that error into campaign approval: a fixed token promise may exceed the intended dollar budget, or the team may allocate fewer tokens than the budget could fund. The USD 1,000-to-USD 1,100 example above illustrates the cost of a 10% upward move while using the old token quantity. Keeping the observation period visible helps the lead judge whether the reference is suitable for the decision being made.
