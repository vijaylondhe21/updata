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

        if underlying_type== 'INDEX':
            opt_symbols = symbol_master[(symbol_master.instrument_type == 'OPTIDX') &  (symbol_master.exchange == 'NSE_FO')]

        elif underlying_type== 'EQUITY':
            underlying_type = 'EQ'
            opt_symbols = symbol_master[(symbol_master.instrument_type == 'OPTSTK') &  (symbol_master.exchange == 'NSE_FO')]
        else :
            return ValueError(f"give underlying_type = `INDEX` or `EQUITY` only not {underlying_type}")
        

        interval = '1minute'
        exchange_str = f'{exchange}_{underlying_type}'
        opt_df = pd.DataFrame()
        for underlying in underlyings:
            underlying_instru_key = symbol_master[(symbol_master.instrument_type == underlying_type) &  (symbol_master.exchange == exchange_str) & (symbol_master.tradingsymbol == underlying)]
            underlying_instru_key = underlying_instru_key['instrument_key'].iloc[0]

            url = f"https://api.upstox.com/v2/historical-candle/intraday/{underlying_instru_key}/{interval}"
            payload={}
            headers = {
            'Accept': 'application/json'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            
            
            if response.status_code == 200:
                response_data = response.json()
                candles_data = response_data['data']['candles']
                columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI']
                underlying_df = pd.DataFrame(candles_data, columns=columns)
                atm_price = underlying_df.iloc[-1]['Close']

                options_df = opt_symbols[(opt_symbols.name == underlying )]
                options_df = options_df.sort_values(by='expiry')
                if strikes != 'all':
                    strikes = int(strikes)
                    options_df['strike'] = pd.to_numeric(options_df['strike'])
                    print(options_df['strike'].dtype)

                    atm_strike = options_df.loc[(options_df['strike'] - atm_price).abs().idxmin(), 'strike']
                    atm_strike_1 = options_df.loc[(options_df['strike'] - atm_price).abs().nsmallest(2).index[0], 'strike']
                    strike_gap = abs(atm_strike - atm_strike_1)
                    print(type(atm_strike), type(strike_gap), type(strikes))

                    options_df = options_df[(options_df.strike <= (atm_strike + (strike_gap * strikes ) )) & (options_df.strike >= (atm_strike - (strike_gap * strikes ) ))]


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
                        if not current_symbol.empty:
                            current_symbol['Symbol'] = options_df['tradingsymbol'][i]
                            # current_symbol['Date'] = pd.to_datetime(current_symbol['Datetime']).dt.date
                            # current_symbol['Time'] = pd.to_datetime(current_symbol['Datetime']).dt.time
                            current_symbol['Interval'] = interval
                            current_symbol['Strike'] = options_df['strike'][i]  
                            current_symbol['Expiry'] = options_df['expiry'][i]
                            current_symbol['Option_type'] = options_df['option_type'][i]
                            current_symbol['Underlying'] = underlying


                            current_symbol = current_symbol[['Symbol', 'Datetime', 'Interval', 'Expiry', 'Option_type', 'Strike', 'Underlying', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI']]
                            opt_df = pd.concat([opt_df, current_symbol], ignore_index=True)
                        
                        print(i, "done")

                    else:
                    # Print an error message if the request was not successful
                        print(f"Error: {response.status_code} - {response.text}")

        return opt_df


# if __name__ == '__main__':

#     upd = UpData()
#     upd.store_options_data(underlyings=['NIFTY'],expiries='latest',strikes='10')
    