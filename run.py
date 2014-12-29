import Quandl
from strategy.RandomForecastingStrategy import RandomForecastingStrategy
from portfolio.MarketOnOpenPortfolio import MarketOnOpenPortfolio

if __name__ == "__main__":
    # Obtain daily bars of SPY (ETF that generally 
    # follows the S&P500) from Quandl (requires 'pip install Quandl'
    # on the command line)
    symbol = 'SPY'
    bars = Quandl.get("GOOG/NYSE_%s" % symbol, collapse="daily")

    # Create a set of random forecasting signals for SPY
    rfs = RandomForecastingStrategy(symbol, bars)
    signals = rfs.generate_signals()

    # Create a portfolio of SPY
    portfolio = MarketOnOpenPortfolio(symbol, bars, signals, initial_capital=100000.0)
    returns = portfolio.backtest_portfolio()

    print returns.tail(10)