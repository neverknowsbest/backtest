import numpy as np
import pandas as pd
import Quandl

from Portfolio import Portfolio

class MarketOnOpenPortfolio(Portfolio):
	"""Inherits Portfolio to create a system that purchases 100 units of
a particular symbol upon a long/short signal, assuming the market
open price of a bar.

In addition, there are zero transaction costs and cash can be immediately
borrowed for shorting (no margin posting or interest requirements).

Requires:
symbol - A stock symbol which forms the basis of the portfolio.
bars - A DataFrame of bars for a symbol set.
signals - A pandas DataFrame of signals (1, 0, -1) for each symbol.
initial_capital - The amount in cash at the start of the portfolio."""

	def __init__(self, symbol, bars, signals, initial_capital=100000.0):
		self.symbol = symbol
		self.bars = bars
		self.signals = signals
		self.initial_capital = float(initial_capital)
		self.positions = self.generate_positions()

	def generate_positions(self):
		"""Creates a 'positions' DataFrame that simply longs or shorts
		  100 of the particular symbol based on the forecast signals of
		  {1, 0, -1} from the signals DataFrame."""
		positions = pd.DataFrame(index=self.signals.index).fillna(0.0)
		positions[self.symbol] = self.signals['signal'].mul(100)
		# print positions
		return positions

	def backtest_portfolio(self):
		"""Constructs a portfolio from the positions DataFrame by
		  assuming the ability to trade at the precise market open price
		  of each bar (an unrealistic assumption!).

		  Calculates the total of cash and the holdings (market price of
		  each position per bar), in order to generate an equity curve
		  ('total') and a set of bar-based returns ('returns').

		  Returns the portfolio object to be used elsewhere.

		  portfolio - amt of stock owned
		  holdings - cash value of stock owned (at open)
		  cash - remaining cash
		  """

		portfolio = self.positions.cumsum()
		pos_diff = self.positions.diff()
#		print portfolio[590:600]

		portfolio['price'] = self.bars['Open']
		portfolio['holdings'] = portfolio['SPY'].mul(self.bars['Open'], axis=0)
		portfolio['cash'] = self.initial_capital - portfolio['holdings'].cumsum()
		portfolio['total'] = portfolio['cash'].add(portfolio['holdings'], axis=0)
		portfolio['returns'] = portfolio['total'].pct_change()
		portfolio['total_return'] = (portfolio['total'] - self.initial_capital)/self.initial_capital * 100
		return portfolio

