from src.data_fetcher import DataFetcher
from src.strategy import Strategy
from src.trader import Trader
from src.visualizer import Visualizer

def main():
    data_fetcher = DataFetcher('AAPL')
    data = data_fetcher.fetch_historical_data()

    strategy = Strategy(data_fetcher)
    strategy.moving_average_strategy()

    trader = Trader(strategy)
    trader.execute_trades()

    visualizer = Visualizer(strategy, trader)
    visualizer.plot_signals()

    trader.log_final_balance()

if __name__ == "__main__":
    main()
