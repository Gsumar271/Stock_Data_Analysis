'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021

@Student Name  : Wall Street Alchemists

'''

import pandas as pd
import datetime

from stock import Stock
from utils import YahooFinancials, MyYahooFinancials
from discount_cf_model import DiscountedCashFlowModel

def run():
    input_fname = "StockUniverseWithData.csv"
    output_fname = "StockUniverseValuation.csv"

    as_of_date = datetime.date(2021, 6, 15)
    df = pd.read_csv(input_fname)
    #df_symbol = df['Symbol']
    
    # TODO
    #used to build a column of fair_values
    results = []
    #used to build a column of stock prices as of 6/25/21
    stocks = []

    for i in range(len(df)):
        symbol = df.loc[i, 'Symbol']
        #print(symbol)
        #initialize stock object
        stock = Stock(symbol)
        #initialize DCF object
        model = DiscountedCashFlowModel(stock, as_of_date)
        #for variable for using yahoo financials
        yfinancial = MyYahooFinancials(symbol)

        try:
            # to get rid of % sign
            EpsNext5Y = df.loc[i, 'EPS Next 5Y']
            EpsNext5YNew = EpsNext5Y[:-1]
            short_term_growth_rate = float(EpsNext5YNew) / 100
            medium_term_growth_rate = short_term_growth_rate / 2
            long_term_growth_rate = 0.04

            model.set_FCC_growth_rate(short_term_growth_rate, medium_term_growth_rate, long_term_growth_rate)
            #calculate fair value
            fair_value = model.calc_fair_value()

        except(KeyError, TypeError, ValueError):
            fair_value = 'NA'
        #get current stock price
        stock_price = yfinancial.get_current_price()
        print(fair_value)
        results.append(str(fair_value))
        #create stock price column to compare with fair price
        stocks.append(str(stock_price))

    df['Fair value'] = results
    df['Stock price'] = stocks

    # writing into the file
    df.to_csv(output_fname, index=False)

    # ....
    
    # end TODO

    
if __name__ == "__main__":
    run()
