import os


class Trader:
    def __init__(self, strategy, initial_balance=10000, log_file='output/trade_log.txt'):
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions = 0
        self.trade_history = []
        self.log_file = log_file

        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def log_trade(self, action, date, price, shares, balance):
        with open(self.log_file, 'a') as f:
            f.write(f"{date} - {action.upper()} {shares} aktier till {price:.2f} USD. Saldo kvar: {balance:.2f} USD\n")

    def execute_trades(self):
        signals = self.strategy.signals
        for i in range(len(signals)):
            if signals['positions'].iloc[i] == 1.0:
                # Köp
                self.buy(signals.index[i], signals['price'].iloc[i], i)
            elif signals['positions'].iloc[i] == -1.0:
                # Sälj
                self.sell(signals.index[i], signals['price'].iloc[i], i)

        # Automatisk försäljning vid slut
        if self.positions > 0:
            final_price = self.strategy.data_fetcher.get_latest_price()
            self.sell(signals.index[-1], final_price, len(signals) - 1)

    def buy(self, date, price, index):
        if self.balance > price:
            shares_to_buy = self.balance // price
            self.positions += shares_to_buy
            self.balance -= shares_to_buy * price
            self.trade_history.append((index, 'buy', price, shares_to_buy))
            self.log_trade('köp', date.strftime('%Y-%m-%d'), price, shares_to_buy, self.balance)

    def sell(self, date, price, index):
        if self.positions > 0:
            self.balance += self.positions * price
            self.trade_history.append((index, 'sell', price, self.positions))
            self.log_trade('sälj', date.strftime('%Y-%m-%d'), price, self.positions, self.balance)
            self.positions = 0

    def get_final_balance(self):
        return self.balance

    def log_final_balance(self):
        final_balance = self.balance
        profit_percentage = ((final_balance - self.initial_balance) / self.initial_balance) * 100
        with open(self.log_file, 'a') as f:
            f.write(f"\nSlutlig balans: {final_balance:.2f} USD\n")
            f.write(f"Procentuell förändring från start: {profit_percentage:.2f}%\n")
