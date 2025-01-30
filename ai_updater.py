import time
from datetime import datetime

import yfinance as yf


class AIModelUpdater:
    def __init__(self):
        self.last_updated = datetime.now()
        self.params = {
            'rsi_oversold': 30,
            'rsi_overbought': 70
        }

    def run(self):
        while True:
            self.update_params()
            time.sleep(3600)  # Update hourly

    def update_params(self):
        try:
            nifty_data = yf.download("^NSEI", period="1mo")
            volatility = nifty_data.Close.pct_change().std()

            if volatility > 0.02:
                self.params.update({'rsi_oversold': 35, 'rsi_overbought': 65})
            else:
                self.params.update({'rsi_oversold': 30, 'rsi_overbought': 70})

            self.last_updated = datetime.now()
        except Exception as e:
            print(f"AI Update error: {str(e)}")
