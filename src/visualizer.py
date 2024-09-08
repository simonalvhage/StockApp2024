import matplotlib.pyplot as plt
import os


class Visualizer:
    def __init__(self, strategy, trader, output_dir='output'):
        self.strategy = strategy
        self.trader = trader
        self.output_dir = output_dir

        # Skapa output-mappen om den inte finns
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def plot_signals(self):
        signals = self.strategy.signals
        plt.figure(figsize=(10, 5))

        plt.plot(signals['price'], label='Pris', alpha=0.5)
        plt.plot(signals['short_mavg'], label='Kort glidande medelvärde', alpha=0.5)
        plt.plot(signals['long_mavg'], label='Lång glidande medelvärde', alpha=0.5)

        buy_signals = signals.loc[signals['positions'] == 1.0]
        plt.plot(buy_signals.index, buy_signals['price'], '^', markersize=10, color='g', lw=0, label='Köp')

        sell_signals = signals.loc[signals['positions'] == -1.0]
        plt.plot(sell_signals.index, sell_signals['price'], 'v', markersize=10, color='r', lw=0, label='Sälj')

        plt.title(f"Pris och handelsignaler för {self.strategy.data_fetcher.ticker}")
        plt.legend()

        plt.savefig(os.path.join(self.output_dir, 'signals_plot.png'))
        plt.close()
