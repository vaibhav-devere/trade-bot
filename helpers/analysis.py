import numpy as np
import pandas as pd
import talib
import yfinance as yf


class StockAnalyzer:
    def __init__(self, symbol, strategy):
        self.strategy = strategy
        self.symbol = symbols
        self.data = self._get_data()
        self.data_valid = not self.data.empty

    def _get_data(self):
        if self.symbol is None:
            return pd.DataFrame()

        interval = '1d' if self.strategy in ['swing', 'holding'] else '60m'
        period = '3y' if self.strategy == 'holding' else '60d'

        try:
            return yf.download(
                f"{self.symbol}.NS",
                period=period,
                interval=interval,
                progress=False
            )
        except:
            return pd.DataFrame()

    def full_analysis(self):
        return {
            'indicators': self._get_technical_indicators(),
            'patterns': self._detect_patterns(),
            'recommendation': self._generate_recommendation()
        }

    def _get_technical_indicators(self):
        return {
            'rsi': round(talib.RSI(self.data.Close, 14)[-1], 2),
            'macd': round(talib.MACD(self.data.Close)[0][-1], 2),
            'sma_50': round(self.data.Close.rolling(50).mean()[-1], 2),
            'sma_200': round(self.data.Close.rolling(200).mean()[-1], 2),
            'volatility': round(self.data.Close.pct_change().std() * np.sqrt(252), 4)
        }

    def _detect_patterns(self):
        return {
            'head_shoulders': talib.CDLHEADSHOULDERS(self.data.Open, self.data.High,
                                                     self.data.Low, self.data.Close)[-1],
            'engulfing': talib.CDLENGULFING(self.data.Open, self.data.High,
                                            self.data.Low, self.data.Close)[-1]
        }

    def _generate_recommendation(self):
        indicators = self._get_technical_indicators()
        if indicators['rsi'] < 35:
            return "Strong Buy"
        elif indicators['rsi'] > 65:
            return "Strong Sell"
        return "Hold"

    def get_top_stocks(self):
        nifty50 = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR",
                   "KOTAKBANK", "ICICIBANK", "ITC", "SBIN", "ASIANPAINT"]
        return nifty50[:10]
