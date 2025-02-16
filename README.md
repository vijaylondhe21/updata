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

# Initialize Updata
updata = Updata(api_key="your_upstox_api_key")

# Download intraday data for options
upd = UpData()
data = upd.store_options_data(underlyings=['NIFTY'], underlying_type='INDEX', expiries='latest', strikes='10')
```

---

## 🌐 Historical Data Available on the Internet

Here’s a curated list of public sources offering free historical financial data:

1. [NSE India](https://www.nseindia.com/market-data) - Daily market snapshots and historical data.
2. [BSE India](https://www.bseindia.com/) - Equity and derivatives historical data.
3. [Alpha Vantage](https://www.alphavantage.co/) - Free API for global equities and forex.
4. [Quandl](https://www.quandl.com/) - Financial and economic datasets.

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

