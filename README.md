# Updata: Your Market Data Research Ends Here

Welcome to **Updata**, a flexible Python library designed to simplify your Indian financial data research workflow. With Updata, you can effortlessly store daily intraday data for Options, Futures, and Equities. This repository gives you sources for available historical data so you don't have to find it on the internet each time.

---

## Features

**Download Intraday Data:**
-Fetch daily intraday data for Options, Futures, and Equities.
-Store the data locally
-check [examples] section to schedule script, store in CSV, SQlite, duckDB, ArcticDB, Postgres

**Get Historical Data:**
-Seamlessly retrieve historical market data using the **Upstox API** (no need for an Upstox account as of now).
-Supports multiple instruments and exchanges.

**One-Stop Historical Data Hub:**
-Find publicly available financial data in one place.
-Explore the ["Historical Data Available on the Internet"](#-historical-data-available-on-the-internet) section for all free resources.

---

## 🛠️ Installation

```bash
pip install updata
```

---

## Usage

```python
from updata import Updata
import pandas as pd
# Download intraday data for options
upd = UpData()
data = upd.store_options_data(underlyings=['NIFTY'],underlying_type='INDEX', expiries='2',strikes='3')
data.to_csv('data.csv')
```

---

## 📌 TODO

- [x] store_option_data
- [ ] store_cash_data
- [ ] store_future_data
- [ ] add more F&O and intraday sources in Readme.md
- [ ] Splits data
- [ ] Economic News data
- [ ] Events Data
- [ ] Margin Data
- [ ] Lot size change Data
- [ ] Dividend Data
- [ ] Checking data quality

---

## 🌐 Historical Data Available on the Internet

Here’s a curated list of public sources offering free historical financial data:

### Cash Market

| Name          | Description                                      | Frequency | Period | Link |
|---------------|--------------------------------------------------|-----------|--------|------|
| NIFTY-50 Stock Data| At a day-level with pricing and trading values split across .csv files for each stock along with a metadata file with some macro-information about the stocks itself.| Daily| Jan 2000 - Apr 2021| [Visit](https://www.kaggle.com/datasets/rohanrao/nifty50-stock-market-data)|
| BSE & NSE stocks| The data spans the period from 2000 to December 2023 for NSE & BSE. CSV files for each year for each company.| Daily| 2000 - Dec 2023| [Visit](https://www.kaggle.com/datasets/chiragb254/indian-stock-market-complete-dataset-2024)|
|Nifty 500 stocks | Each stock in this Nifty 500 and are of 1 minute itraday data  - Data is updated Weekly| 1 minute| 2015 to 2025| [Visit](https://www.kaggle.com/datasets/debashis74017/algo-trading-data-nifty-100-data-with-indicators)|
|Nifty & BankNifty | Minute by minute OHLC data for two indices (NIFTY and BANKNIFTY) | 1 minute| 2008-2020| [Visit](https://www.kaggle.com/datasets/nishanthsalian/indian-stock-index-1minute-data-2008-2020)|

### Futures and Options

There isn't any data available for free. We'll try to find some data and update here othewise we'll soon upload data stored by us. If you find some useful dataset then contribute by raising issue and mentioning the URL of dataset.

---

## Disclaimer

- I do not own this data and I am not selling this data.
- This data is intended for **research purposes only**.
- I am not affiliated with Upstox, NSE, or any other exchange mentioned anywhere in this package.

---

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

## ✨ Stay Connected

- 🐦 Follow us on Socials.
- ![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?logo=twitter&logoColor=white) [Vijay](https://x.com/kon_vijay)
- ![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white) [Vijay](https://www.linkedin.com/in/vijaylondhe)
- ![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white) [Parul](https://www.linkedin.com/in/parulkakade)
