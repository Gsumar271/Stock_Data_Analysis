'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Elaine Chen

@Date          : June 2021


'''

import datetime
from scipy.stats import norm
from math import gamma, log, exp, pi, sqrt

from stock import Stock
from option import Option, EuropeanCallOption

class BlackScholesModel(object):
    '''
    OptionPricer
    '''

    def __init__(self, pricing_date, risk_free_rate):
        self.pricing_date = pricing_date
        self.risk_free_rate = risk_free_rate

    def calc_parity_price(self, option, option_price):
        '''
        return the put price from Put-Call Parity if input option is a call
        else return the call price from Put-Call Parity if input option is a put
        '''
        result = None
        # TODO: implement details here
        cp = option.strike * exp(-1 * self.risk_free_rate * option.time_to_expiry)
        if option.option_type == Option.Type.CALL:
            result = option_price - option.underlying.spot_price + cp
        elif option.option_type == Option.Type.PUT: 
            result = option_price + option.underlying.spot_price - cp
        # end TODO
        return(result)

    def calc_model_price(self, option):
        '''
        Calculate the price of the option using Black-Scholes model
        '''
        px = None
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate

            #TODO: implement details here
            d1 = (log(S0 / K) + T * (r - q + pow(sigma, 2)/2)) / (sigma * sqrt(T))
            d2 = d1 - (sigma * sqrt(T))

            if option.option_type == Option.Type.CALL:
                px = S0 * exp(-q * T) * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
            elif option.option_type == Option.Type.PUT: 
                px = K * exp(-r * T) * norm.cdf(-d2) - S0 * exp(-q * T) * norm.cdf(-d1)
            #end TODO
        else:
            raise Exception("Unsupported option type")        
        return(px)

    def calc_delta(self, option):
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            # TODO:
            d1 = (log(option.underlying.spot_price / option.strike) + option.time_to_expiry * (self.risk_free_rate - option.underlying.dividend_yield + pow(option.underlying.sigma, 2)/2)) / (option.underlying.sigma * sqrt(option.time_to_expiry))
            if option.option_type == Option.Type.CALL:
                result = exp(-option.underlying.dividend_yield * option.time_to_expiry) * norm.cdf(d1)
            elif option.option_type == Option.Type.PUT: 
                result = -exp(-option.underlying.dividend_yield * option.time_to_expiry) * norm.cdf(d1)
            # end TODO
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_gamma(self, option):

        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            # TODO:
            d1 = (log(option.underlying.spot_price / option.strike) + option.time_to_expiry * (self.risk_free_rate - option.underlying.dividend_yield + pow(option.underlying.sigma, 2)/2)) / (option.underlying.sigma * sqrt(option.time_to_expiry))
            if option.option_type == Option.Type.CALL:
                result = (exp(-option.underlying.dividend_yield * option.time_to_expiry) / (option.underlying.spot_price * option.underlying.sigma * sqrt(option.time_to_expiry))) * (1 / sqrt(2 * pi)) * exp(pow(-d1, 2)/2)
            elif option.option_type == Option.Type.PUT:
                result = (exp(-option.underlying.dividend_yield * option.time_to_expiry) / (option.underlying.spot_price * option.underlying.sigma * sqrt(option.time_to_expiry))) * (1 / sqrt(2 * pi)) * exp(pow(-d1, 2)/2)

            # end TODO
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_theta(self, option):
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:

            # TODO:
            d1 = (log(option.underlying.spot_price / option.strike) + option.time_to_expiry * (self.risk_free_rate - option.underlying.dividend_yield + pow(option.underlying.sigma, 2)/2)) / (option.underlying.sigma * sqrt(option.time_to_expiry))
            d2 = d1 - (option.underlying.sigma * sqrt(option.time_to_expiry))
            if option.option_type == Option.Type.CALL:
                result = (1 / option.time_to_expiry) * (-((option.underlying.spot_price * option.underlying.sigma * exp(-option.underlying.dividend_yield * option.time_to_expiry)) / (2 * sqrt(option.time_to_expiry))) * (1 / sqrt(2 * pi)) * exp(pow(-d1, 2)/2) - self.risk_free_rate * option.strike * exp(-self.risk_free_rate * option.time_to_expiry) * norm.cdf(d2) + option.underlying.dividend_yield * option.underlying.spot_price * exp(-option.underlying.dividend_yield * option.time_to_expiry) * norm.cdf(d1))
            elif option.option_type == Option.Type.PUT:
                result = (1 / option.time_to_expiry) * (-((option.underlying.spot_price * option.underlying.sigma * exp(-option.underlying.dividend_yield * option.time_to_expiry)) / (2 * sqrt(option.time_to_expiry))) * (1 / sqrt(2 * pi)) * exp(pow(-d1, 2)/2) + self.risk_free_rate * option.strike * exp(-self.risk_free_rate * option.time_to_expiry) * norm.cdf(-d2) - option.underlying.dividend_yield * option.underlying.spot_price * exp(-option.underlying.dividend_yield * option.time_to_expiry) * norm.cdf(-d1))
            # end TODO
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_vega(self, option):
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            # TODO:
            d1 = (log(option.underlying.spot_price / option.strike) + option.time_to_expiry * (self.risk_free_rate - option.underlying.dividend_yield + pow(option.underlying.sigma, 2)/2)) / (option.underlying.sigma * sqrt(option.time_to_expiry))
            if option.option_type == Option.Type.CALL:
                result = (1 / 100) * option.underlying.spot_price * exp(-option.underlying.dividend_yield * option.time_to_expiry) * sqrt(option.time_to_expiry) * (1 / sqrt(2 * pi)) * exp(pow(-d1, 2)/2)
            elif option.option_type == Option.Type.PUT:
                result = (1 / 100) * option.underlying.spot_price * exp(-option.underlying.dividend_yield * option.time_to_expiry) * sqrt(option.time_to_expiry) * (1 / sqrt(2 * pi)) * exp(pow(-d1, 2)/2)
            # end TODO
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_rho(self, option):
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            # TODO:
            d1 = (log(option.underlying.spot_price / option.strike) + option.time_to_expiry * (self.risk_free_rate - option.underlying.dividend_yield + pow(option.underlying.sigma, 2)/2)) / (option.underlying.sigma * sqrt(option.time_to_expiry))
            d2 = d1 - (option.underlying.sigma * sqrt(option.time_to_expiry))
            if option.option_type == Option.Type.CALL:
                result = 0.01 * (option.strike * option.time_to_expiry * exp(-self.risk_free_rate * option.time_to_expiry) * norm.cdf(d2))
            elif option.option_type == Option.Type.PUT: 
                result = -0.01 * (option.strike * option.time_to_expiry * exp(-self.risk_free_rate * option.time_to_expiry) * norm.cdf(-d2))
            # end TODO
        else:
            raise Exception("Unsupported option type")
        return result


def _test():

    symbol = 'AAPL'
    pricing_date = datetime.date(2021, 6, 1)

    risk_free_rate = 0.01
    model = BlackScholesModel(pricing_date, risk_free_rate)

    # .... use this as your unit test
    # calculate the B/S model price for a 3-month ATM call

    T = 3/12
    num_period = 2

    dt = T / num_period
    S0 = 50
    K = 50

    sigma = 0.3
    
    stock = Stock(symbol, S0, sigma)
    
    # call = EuropeanCallOption(stock, dt, K)
    call = EuropeanCallOption(stock, T, K)

    model_price = model.calc_model_price(call)
    delta = model.calc_delta(call)
    gamma = model.calc_gamma(call)
    theta = model.calc_theta(call)
    vega = model.calc_vega(call)
    rho = model.calc_rho(call)
    parity = model.calc_parity_price(call, model_price)

    print("Parity-Price: ", parity)
    print("Model Price: ", model_price)
    print("Delta: ", delta)
    print("Gamma: ", gamma)
    print("Theta: ", theta)
    print("Vega: ", vega)
    print("Rho: ", rho)


if __name__ == "__main__":
    _test()
    
