'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Yevgeniy Sumaryev

@Date          : June 2021

Discounted Cash Flow Model with Financial Data from Yahoo Financial

https://medium.datadriveninvestor.com/how-to-calculate-intrinsic-value-of-a-stock-aapl-case-study-935fb062004b

'''
import enum
import calendar
import math
import pandas as pd
import numpy as np

import datetime 
from scipy.stats import norm

from math import log, exp, sqrt
from stock import Stock


class DiscountedCashFlowModel(object):
    '''
    DCF Model:

    FCC is assumed to go have growth rate by 3 periods, each of which has different growth rate
           short_term_growth_rate for the next 5Y
           medium_term_growth_rate from 6Y to 10Y
           long_term_growth_rate from 11Y to 20thY
    '''

    #constructor
    def __init__(self, stock, as_of_date):
        self.stock = stock
        self.as_of_date = as_of_date

        self.short_term_growth_rate = None
        self.medium_term_growth_rate = None
        self.long_term_growth_rate = None

    #set growth rate variables
    def set_FCC_growth_rate(self, short_term_rate, medium_term_rate, long_term_rate):
        self.short_term_growth_rate = short_term_rate
        self.medium_term_growth_rate = medium_term_rate
        self.long_term_growth_rate = long_term_rate


    def calc_fair_value(self):
        '''
        calculate the fair_value using DCF model

        1. calculate a yearly discount factor using the WACC
        2. Get the Free Cash flow
        3. Sum the discounted value of the FCC for the first 5 years using the short term growth rate
        4. Add the discounted value of the FCC from year 6 to the 10th year using the medium term growth rate
        5. Add the discounted value of the FCC from year 10 to the 20th year using the long term growth rate
        6. Compute the PV as cash + short term investments - total debt + the above sum of discounted free cash flow
        7. Return the stock fair value as PV divided by num of shares outstanding

        '''
        #TODO
        result = 0
        #get all necessary data
        beta = self.stock.get_beta()
        WACC = self.stock.lookup_wacc_by_beta(beta)
        FCC = self.stock.get_free_cashflow()
        DF = 1 / (1 + WACC)
        EPS5Y = self.short_term_growth_rate
        EPS6To10Y = self.medium_term_growth_rate
        EPS10To20Y = self.long_term_growth_rate

        #calculate DCF
        DCF = 0
        for i in range(1, 6):
            DCF += FCC * (1 + EPS5Y) ** i * DF ** i

        CF5 = FCC * (1 + EPS5Y) ** 5
        for i in range(1, 6):
            DCF += CF5 * (1 + EPS6To10Y) ** i * DF ** (i + 5)

        CF10 = CF5 * (1 + EPS6To10Y) ** 5
        for i in range(1, 11):
            DCF += CF10 * (1 + EPS10To20Y) ** i * DF ** (i + 10)
        #end TODO
        #calculate fair value according to the formula from class
        PV = self.stock.get_cash() - self.stock.get_total_debt() + DCF
        shares = self.stock.get_num_shares_outstanding()
        result = PV/shares


        return result


def _test():
    symbol = 'AAPL'
    as_of_date = datetime.date(2021, 4, 19)

    stock = Stock(symbol)
    model = DiscountedCashFlowModel(stock, as_of_date)

    print("Shares ", stock.get_num_shares_outstanding())

    # look up from Finviz
    eps5y = 0.14
    model.set_FCC_growth_rate(eps5y, eps5y/2, 0.04)

    model_price = model.calc_fair_value()
    print(model_price)

if __name__ == "__main__":
    _test()
