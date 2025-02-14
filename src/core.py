
class UpData:
    def __init__(self, source='UPSTOX', types=['OPTIONS'], exchange= 'NSE'):
        self.source = source
        self.exchange = 'NSE'
        if self.source == 'UPSTOX' and self.exchange == 'NSE' :
            self.symbol_master_link = 'https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz'


def store_options_data(self, underlyings: list, expiries: str = 'latest', strikes: str = '10'):
    """
    Stores options data for the given underlyings and expiries.

    Args:
        underlyings (list): **Required.** List of underlying indices or stocks for which data will be stored.  
            Use `UpData.list_opt_underlyings()` to view available underlyings.
        expiries (str, optional): Defines which expiries to store. Defaults to `'latest'`.  
            - `'latest'`: Only stores the current expiry.  
            - `'month'`: Stores all expiries within the current month.  
            - `'all'`: Stores all available expiries.  
        strikes (str, optional): Defines which strikes to store. Defaults to `'10'`.  
            - `'10'`: Stores ATM ± 10 strikes. Can specify any number. ATM is assumed at the **9:15 AM open price**.  
            - `'all'`: Stores all available strikes.  

    Returns:
        DataFrame 
    """



