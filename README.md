# Updata: Your Financial Data Research Ends Here

Welcome to **Updata**, a flexible Python library designed to simplify your Indian financial data research workflow. With Updata, you can effortlessly store daily intraday data for Options, Futures, and Equities. This repository gives you sources for available historical data so you don't have to find it on the internet each time.

---

## 🚀 Features

✅ **Download Intraday Data:**
- Fetch daily intraday data for Options, Futures, and Equities.
- Store the data locally for faster analysis and backtesting.

✅ **Get Historical Data:**
- Seamlessly retrieve historical market data using the **Upstox API** (no need for an Upstox account as of now).
- Supports multiple instruments and exchanges.

✅ **One-Stop Historical Data Hub:**
- Find and aggregate publicly available financial data in one place.
- Explore the "Historical Data Available on the Internet" section for free resources.

---

## 🛠️ Installation

```bash
pip install updata
```

Or, if you want the latest development version:

```bash
git clone https://github.com/yourusername/updata.git
cd updata
pip install -e .
```

---

## 📈 Usage

```python
from updata import Updata

# Download intraday data for options
upd = UpData()
data = upd.store_options_data(underlyings=['NIFTY'], underlying_type='INDEX', expiries='latest', strikes='10')
```

---

## 🌐 Historical Data Available on the Internet

Here’s a curated list of public sources offering free historical financial data:

### 💰 Cash Market

| Name          | Description                                      | Frequency | Period | Link |
|---------------|--------------------------------------------------|-----------|--------|------|
| NIFTY-50 Stock Data| At a day-level with pricing and trading values split across .csv files for each stock along with a metadata file with some macro-information about the stocks itself. | Daily | Jan 2000 - Apr 2021 | [Visit](https://www.kaggle.com/datasets/rohanrao/nifty50-stock-market-data) |
| BSE & NSE stocks | The data spans the period from 2000 to December 2023 for NSE & BSE. CSV files for each year for each company. | Daily | 2000 - Dec 2023 | [Visit](https://www.kaggle.com/datasets/chiragb254/indian-stock-market-complete-dataset-2024) |

### 📈 Futures and Options

| Name          | Description                                      | Frequency | Period | Link |
|---------------|--------------------------------------------------|-----------|--------|------|
| Upstox | Free API for global equities and forex.         | Daily | Ongoing | [Visit](https://www.alphavantage.co/) |
| nan        | Financial and economic datasets.                | Daily | Ongoing | [Visit](https://www.quandl.com/) |

---




## 💡 Disclaimer

- I do not own this data and I am not selling this data.
- This data is intended for **research purposes only**.
- I am not affiliated with Upstox, NSE, or any other exchange in India.

---

## 🌜 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

## ✨ Stay Connected

- ⭐ Star this repository to show your support!
- 🐦 Follow us on Twitter for updates and financial insights.

---

**Updata — Your Financial Data Research Ends Here.**

---

Let me know if you’d like to add badges, GitHub actions, or a logo for a more polished look!

