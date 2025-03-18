import requests
import logging

from datetime import datetime
import pandas as pd

logging.basicConfig(level=logging.INFO)

class UpData:
    '''
    Currently source for fetching data is Upstox as they are providing data without the need of login. If upstox change this policy in future and requires user to login via API key then we'll find some new source or use NSE bhavcopy.
    '''
    def __init__(self, source='UPSTOX'):
        self.source = source
        if self.source == 'UPSTOX':
            self.symbol_master_link = 'https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz'
            self.holiday_link =  "https://api.upstox.com/v2/market/holidays/:date"
        
    


    def store_options_data(self, underlyings: list, underlying_type : str, expiries: str = '1', strikes: str = '5', exchange : str = 'NSE'):
        """
        Fetch options data for the given underlyings and expiries.

        Args:
            underlyings (list[],  **Required.**): List of underlying indices or stocks for which data will be stored.  
                Use `UpData.list_opt_underlyings()` to view available underlyings.
            underlying_type (str, **Required.**):  
                - `'INDEX'`: given underlyings are INDEX.
                - `'EQUITY'`: given underlyings are EQUITY.
            expiries (str, optional): Defines which expiries to store. Defaults to `'0'`.  
                - `'1'`: store only recent expiry.  
                - `'2'`: store recent + 1. Any number can be given  
                - `'all'`: Stores all available expiries.  
            strikes (str, optional): Defines which strikes to store. Defaults to `'10'`.  
                - `'5'`: Stores ATM ± 5 strikes. Can specify any number. ATM is assumed at the **9:15 AM Open price**.  
                - `'all'`: Stores all available strikes.  
            exchange (str , **Required.**):  Exhnage to download data from. currently only NSE is supported  
                - `'NSE'`: National Stock Exchange.    

        Returns: 
            DataFrame 
        """         
        today_date = datetime.today().strftime('%Y-%m-%d')
        market_status_url = f"https://api.upstox.com/v2/market/timings/{today_date}"
        payload={}
        headers = {
        'Accept': 'application/json'
        }

        status_response = requests.request("GET", market_status_url, headers=headers, data=payload)
        status_response = status_response.json()


        if status_response.get("data") and any(entry["exchange"] == exchange for entry in status_response.get("data", [])):

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
                    latest_expiry = options_df['expiry'].min()
                    if expiries != 'all':
                        expiries = int(expiries)
                        all_expiries = options_df['expiry'].unique()
                        all_expiries = all_expiries[:expiries]
                        options_df = options_df[(options_df.expiry <= all_expiries[-1])]

                    if strikes != 'all':
                        strikes = int(strikes)
                        options_df['strike'] = pd.to_numeric(options_df['strike'])
                        
                        # selected latest expiry and only CE to get strike list and strike gap
                        temp_options_df = options_df[(options_df.option_type =='CE') & (options_df.expiry == latest_expiry)]
                        strike_list = pd.Series(temp_options_df['strike'].unique())
                        strike_list_diff = (strike_list - atm_price).abs()
                        closest_idx = strike_list_diff.idxmin()
                        second_closest_idx = strike_list_diff.nsmallest(2).idxmax()  
                        atm_strike = strike_list[closest_idx]
                        atm_strike_1 = strike_list[second_closest_idx]
                        strike_gap = abs(atm_strike - atm_strike_1)

                        upper_strike = atm_strike + (strike_gap * strikes ) 
                        lower_strike = atm_strike - (strike_gap * strikes ) 
                        strike_range = options_df['strike'].between(lower_strike,upper_strike , inclusive = 'both')
                        options_df = options_df[strike_range]

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
                                current_symbol = current_symbol.sort_values(by='Datetime')
                                opt_df = pd.concat([opt_df, current_symbol], ignore_index=True)
                            
                            print(i, "done")

                        else:
                        # Print an error message if the request was not successful
                            print(f"Error: {response.status_code} - {response.text}")
            opt_df.reset_index(inplace=True, drop=True)
                            
            return opt_df
        else :
            logging.info("Looks like today is a market holiday, hence no data.")
            return pd.DataFrame()    
        
    def store_cash_data(self, symbols :list, exchange : str = 'NSE', symbol_type: str = 'INDEX'):
        """
        description
        """
        symbol_master = pd.read_csv(self.symbol_master_link)
        cash_symbols = pd.DataFrame()

        if symbol_type== 'INDEX':
            instru_type = 'INDEX'
            exchange_str = f'{exchange}_{instru_type}'
            cash_symbols = symbol_master[(symbol_master.instrument_type == 'INDEX') & (symbol_master.exchange == exchange_str)]
            cash_symbols = cash_symbols[cash_symbols['tradingsymbol'].isin(symbols)]

        elif symbol_type== 'EQUITY':
            instru_type = 'EQ'
            exchange_str = f'{exchange}_{instru_type}'
            cash_symbols = symbol_master[(symbol_master.instrument_type == 'EQUITY')& (symbol_master.exchange == exchange_str)]
            cash_symbols = cash_symbols[cash_symbols['tradingsymbol'].isin(symbols)]
        else :
            return ValueError(f"give underlying_type = `INDEX` or `EQUITY` only not {instru_type}")

        cash_df = pd.DataFrame() 

        for i in cash_symbols.index:           
            instrument_key = cash_symbols['instrument_key'][i]
            interval = '1minute'
            url = f'https://api.upstox.com/v2/historical-candle/intraday/{instrument_key}/{interval}'
            headers = {'Accept': 'application/json'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                candles_data = response_data['data']['candles']
                columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume' , 'OI']
                current_symbol = pd.DataFrame(candles_data, columns=columns)
                current_symbol['Datetime'] = pd.to_datetime(current_symbol['Datetime'])
                current_symbol['Interval'] = interval
                current_symbol['Symbol'] = cash_symbols['tradingsymbol'][i]
                current_symbol['Exchange'] = (instrument_key).split('|')[0]
                fname=(instrument_key).split('|')[1]
                current_symbol = current_symbol[['Symbol','Datetime', 'Interval', 'Open', 'High', 'Low', 'Close', 'Volume', 'Exchange']]
                current_symbol.sort_values(by='Datetime')
                cash_df = pd.concat([cash_df, current_symbol], ignore_index=True)
                print(f"Intraday data for {instrument_key} done.")
            else:
                print(f"Error fetching intraday data: {response.status_code} - {response.text}")
        cash_df.reset_index(inplace=True, drop=True)
        return cash_df


        