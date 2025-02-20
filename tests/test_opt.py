import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from updata import UpData

upd = UpData()
dd = upd.store_options_data(underlyings=['NIFTY'],underlying_type='INDEX', expiries='latest',strikes='3')
dd.to_csv('hh.csv')
# upd.print_it(st='kkk')