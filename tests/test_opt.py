import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from updata import UpData

upd = UpData()
dd = upd.store_options_data(underlyings=['NIFTY'],underlying_type='INDEX', expiries='2',strikes='3')
# dd = upd.store_cash_data(symbols=['ADANIPOWER', 'TATACHEM' ], exchange='NSE', symbol_type='EQUITY')
dd.to_csv('hh1.csv')
# upd.print_it(st='kkk')