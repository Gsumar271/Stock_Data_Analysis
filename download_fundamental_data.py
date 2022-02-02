import pandas as pd
# from utils import yahoofinancials, MyYahooFinancials
import yfinance as yf
import requests
from utils import YahooFinancials, MyYahooFinancials
from stock import Stock
from bs4 import BeautifulSoup as bs


def download_fundamental_data(input_file_name, output_file_name):
    '''

    '''
    #read in input file
    df_orig = pd.read_csv(input_file_name)
    df_symbol = df_orig['Symbol']
    # TODO
    df_new = df_orig.copy(deep=True)
    #for each row in input file
    for i in range(len(df_symbol)):
        ticker = df_symbol[i]
        print(ticker)

        yfinance = MyYahooFinancials(ticker)
        stock = Stock(ticker)
        url = ("http://finviz.com/quote.ashx?t=" + ticker.lower())
        #use beautiful soup library to scraoe data from finviz to get Sector
        #and EPS data
        soup = bs(requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}).content,
                  'html.parser')
        #use try/catch to deal with unavailable data
        #if data is unavailable output NA into cell
        try:
            df_new.loc[i, ['Sector']] = yf.Ticker(ticker).info['sector']
        except (KeyError,TypeError):
            df_new.loc[i, ['Sector']] = 'NA'

        try:
            df_new.loc[i, ['EPS Next 5Y']] = soup.find(text='EPS next 5Y').find_next(class_='snapshot-td2').text
        except (KeyError,TypeError):
            df_new.loc[i, ['EPS Next 5Y']] = 'NA'
        try:
            df_new.loc[i, ['Market Cap']] = soup.find(text='Market Cap').find_next(class_='snapshot-td2').text
        except (KeyError,TypeError):
            df_new.loc[i, ['Market Cap']] = 'NA'

        try:
            df_new.loc[i, 'Total Assets'] = str(yfinance.get_total_assets())
        except (KeyError,TypeError):
            df_new.loc[i, 'Total Assets'] = 'NA'

        try:
            df_new.loc[i, 'Total Debts'] = str(stock.get_total_debt())
        except (KeyError,TypeError):
            df_new.loc[i, 'Total Debts'] = 'NA'

        try:
            df_new.loc[i, 'Free Cash Flow'] = str(stock.get_free_cashflow())
        except (KeyError,TypeError):
            df_new.loc[i, 'Free Cash Flow'] = 'NA'

        try:
            df_new.loc[i, 'Beta'] = str(yfinance.get_beta())
        except (KeyError,TypeError):
            df_new.loc[i, 'Beta'] = 'NA'

        try:
            df_new.loc[i, 'P/E Ratio'] = str(yfinance.get_pe_ratio())
        except (KeyError,TypeError):
            df_new.loc[i, 'P/E Ratio'] = 'NA'

    '''
    Fill in the missing data with NA
    '''
    for i in range(len(df_symbol)):
        for j in range(9):
            if df_new.iloc[i][j] is None:
                df_new.iat[i, j] = 'NA'

    df_new.to_csv(output_file_name, index=False)
    print(df_new)
    # end TODO


def run():
    input_fname = "StockUniverse.csv"
    output_fname = "StockUniverseWithData.csv"

    download_fundamental_data(input_fname, output_fname)


if __name__ == "__main__":
    run()
