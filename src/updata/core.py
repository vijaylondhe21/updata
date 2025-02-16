import requests
import os
import pandas as pd
import inspect
import re
# url = "https://api.upstox.com/v2/historical-candle/intraday/:instrument_key/:interval"

# payload={}
# headers = {
#   'Accept': 'application/json'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

class UpData:
    def __init__(self, source='UPSTOX'):
        self.source = source
        if self.source == 'UPSTOX':
            self.symbol_master_link = 'https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz'


    def print_it(self,st):
        print(st)

    def store_options_data(self, underlyings: list, underlying_type : str, expiries: str = 'latest', strikes: str = '10', exchange : str = 'NSE'):
        """
        Stores options data for the given underlyings and expiries.

        Args:
            underlyings (list[],  **Required.**): List of underlying indices or stocks for which data will be stored.  
                Use `UpData.list_opt_underlyings()` to view available underlyings.
            underlying_type (str, **Required.**):  
                - `'INDEX'`: given underlyings are INDEX.
                - `'EQUITY'`: given underlyings are EQUITY.
            expiries (str, optional): Defines which expiries to store. Defaults to `'latest'`.  
                - `'latest'`: Only stores the current expiry.  
                - `'month'`: Stores all expiries within the current month.  
                - `'all'`: Stores all available expiries.  
            strikes (str, optional): Defines which strikes to store. Defaults to `'10'`.  
                - `'10'`: Stores ATM ± 10 strikes. Can specify any number. ATM is assumed at the **9:15 AM Open price**.  
                - `'all'`: Stores all available strikes.  
            exchange (str , **Required.**):  Exhnage to download data from. currently only NSE is supported  
                - `'NSE'`: National Stock Exchange.  

        Returns:
            DataFrame 
        """
        # # Store CSV in same directory where this function is called
        # caller_frame = inspect.stack()[1]  
        # caller_filename = caller_frame.filename  
        # caller_dir = os.path.dirname(os.path.abspath(caller_filename))  

        # print(f"Saving Master CSV in: {caller_dir}")

        symbol_master = pd.read_csv(self.symbol_master_link)
        
        opt_symbols = pd.DataFrame()
        opt_df = pd.DataFrame()
        if underlying_type== 'INDEX':
            opt_symbols = symbol_master[(symbol_master.instrument_type == 'OPTIDX') &  (symbol_master.exchange == 'NSE_FO')]

        elif underlying_type== 'EQUITY':
            underlying_type = 'EQ'
            opt_symbols = symbol_master[(symbol_master.instrument_type == 'OPTSTK') &  (symbol_master.exchange == 'NSE_FO')]
        else :
            return ValueError(f"give underlying_type = `INDEX` or `EQUITY` only not {underlying_type}")
        

        interval = '1minute'
        exchange_str = f'{exchange}_{underlying_type}'
        for underlying in underlyings:
            underlying_instru_key = symbol_master[(symbol_master.instrument_type == underlying_type) &  (symbol_master.exchange == exchange_str) & (symbol_master.tradingsymbol == underlying)]
            url = f"https://api.upstox.com/v2/historical-candle/intraday/{underlying_instru_key}/{interval}"
            payload={}
            headers = {
            'Accept': 'application/json'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            options_df = opt_symbols[(opt_symbols.name == underlying )]
            if response.status_code == 200:
                for i in options_df.index:
                    
                    instrument_key =  options_df['instrument_key'][i]
                    url = f"https://api.upstox.com/v2/historical-candle/intraday/{instrument_key}/{interval}"
                    payload={}
                    headers = {
                    'Accept': 'application/json'
                    }

                    response = requests.request("GET", url, headers=headers, data=payload)
                    if response.status_code == 200:
                        response_data = response.json()
                        candles_data = response_data['data']['candles']
                        columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI']
                        
                        current_symbol = pd.DataFrame(candles_data, columns=columns)
                        current_symbol['Symbol'] = options_df['tradingsymbol'][i]
                        # current_symbol['Date'] = pd.to_datetime(current_symbol['Datetime']).dt.date
                        # current_symbol['Time'] = pd.to_datetime(current_symbol['Datetime']).dt.time
                        current_symbol['Interval'] = interval
                        current_symbol['Strike'] = options_df['strike'][i]  
                        current_symbol['Expiry'] = options_df['expiry'][i]
                        current_symbol['Option_type'] = options_df['option_type'][i]
                        current_symbol['Underlying'] = underlying


                        current_symbol = current_symbol[['Symbol', 'Datetime', 'Interval', 'Expiry', 'Option_type', 'Strike', 'Underlying', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI']]
                        # current_symbol.to_sql('tbl_options', con=engine, if_exists='append', INDEX=False)
                        
                        print(i, "done")
                        opt_df = pd.concat([opt_df, current_symbol], ignore_index=True)

                    else:
                    # Print an error message if the request was not successful
                        print(f"Error: {response.status_code} - {response.text}")

        return opt_df


# if __name__ == '__main__':

#     upd = UpData()
#     upd.store_options_data(underlyings=['NIFTY'],expiries='latest',strikes='10')
    