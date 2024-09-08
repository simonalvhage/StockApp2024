import numpy as np
import pandas as pd


class Strategy:
    def __init__(self, data_fetcher):
        self.data_fetcher = data_fetcher
        self.signals = pd.DataFrame()

    def moving_average_strategy(self, short_window=40, long_window=100):
        # Enkel glidande medelvärdesstrategi.
        data = self.data_fetcher.stock_data
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']
        signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
        signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

        # köp och säljsignaler
        signals['signal'] = 0.0
        signals['signal'][short_window:] = np.where(
            signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
        signals['positions'] = signals['signal'].diff()

        self.signals = signals
        return signals
