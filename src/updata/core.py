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
    def __init__(self, source='UPSTOX', types=['OPTIONS'], exchange= 'NSE'):
        self.source = source
        self.exchange = 'NSE'
        if self.source == 'UPSTOX' and self.exchange == 'NSE' :
            self.symbol_master_link = 'https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz'


    def print_it(self,st):
        print(st)

    def store_options_data(self, underlyings: list, underlying_type : str, expiries: str = 'latest', strikes: str = '10'):
        """
        Stores options data for the given underlyings and expiries.

        Args:
            underlyings (list): **Required.** List of underlying indices or stocks for which data will be stored.  
                Use `UpData.list_opt_underlyings()` to view available underlyings.
            underlying_type (str):
                - `'index'`: given underlyings are index.
                - `'stock'`: given underlyings are stocks.
            expiries (str, optional): Defines which expiries to store. Defaults to `'latest'`.  
                - `'latest'`: Only stores the current expiry.  
                - `'month'`: Stores all expiries within the current month.  
                - `'all'`: Stores all available expiries.  
            strikes (str, optional): Defines which strikes to store. Defaults to `'10'`.  
                - `'10'`: Stores ATM ± 10 strikes. Can specify any number. ATM is assumed at the **9:15 AM Open price**.  
                - `'all'`: Stores all available strikes.  

        Returns:
            DataFrame 
        """
        # # Store CSV in same directory where this function is called
        # caller_frame = inspect.stack()[1]  
        # caller_filename = caller_frame.filename  
        # caller_dir = os.path.dirname(os.path.abspath(caller_filename))  

        # print(f"Saving Master CSV in: {caller_dir}")

        symbol_master = pd.read_csv('https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz')
        
        # print(symbol_master)
        # save_path = os.path.join(caller_dir, 'symbol_master.csv')
        # symbol_master.to_csv(save_path, index=False)
        opt_symbols = pd.DataFrame()
        opt_df = pd.DataFrame()
        if underlying_type== 'index':
            opt_symbols = symbol_master[(symbol_master.instrument_type == 'OPTIDX') &  (symbol_master.exchange == 'NSE_FO')]
        elif underlying_type== 'stock':
            opt_symbols = symbol_master[(symbol_master.instrument_type == 'OPTSTK') &  (symbol_master.exchange == 'NSE_FO')]
        else :
            return ValueError(f"give underlying_type = `index` or `stock` only not {underlying_type}")
        

        interval = '1minute'
        for underlying in underlyings:
            options_df = opt_symbols[(opt_symbols.name == underlying )]
            
            for i in options_df.index:
                
                instrument_key =  options_df['instrument_key'][i]
                url = f"https://api.upstox.com/v2/historical-candle/intraday/:{instrument_key}/:{interval}"
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
                    current_symbol['Instrument'] = options_df['tradingsymbol'][i]
                    # current_symbol['Date'] = pd.to_datetime(current_symbol['Datetime']).dt.date
                    # current_symbol['Time'] = pd.to_datetime(current_symbol['Datetime']).dt.time
                    current_symbol['Interval'] = interval
                    current_symbol['Strike'] = options_df['strike'][i]  
                    current_symbol['Expiry'] = options_df['expiry'][i]
                    current_symbol['Option_type'] = options_df['option_type'][i]
                    current_symbol['Underlying'] = underlying


                    current_symbol = current_symbol[['Instrument', 'Datetime', 'Interval', 'Expiry', 'Option_type', 'Strike', 'Underlying', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI']]
                    # current_symbol.to_sql('tbl_options', con=engine, if_exists='append', index=False)
                    
                    print(i, "done")
                    opt_df = pd.concat([opt_df, current_symbol], ignore_index=True)

                else:
                # Print an error message if the request was not successful
                    print(f"Error: {response.status_code} - {response.text}")

        return opt_df


# if __name__ == '__main__':

#     upd = UpData()
#     upd.store_options_data(underlyings=['NIFTY'],expiries='latest',strikes='10')
    