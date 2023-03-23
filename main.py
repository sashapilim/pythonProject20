import time
from binance.client import Client


class PriceMonitor:
    def __init__(self, api_key, api_secret, symbol):
        self.client = Client(api_key, api_secret)
        self.symbol = symbol
        self.prev_price = None

    def get_eth_price(self):
        # Get the latest prices of the BTCUSDT and ETHUSDT futures
        btc_price = float(self.client.futures_symbol_ticker('BTCUSDT')['price'])
        eth_price = float(self.client.futures_symbol_ticker('ETHUSDT')['price'])

        # Use the regression model to isolate the movements of the ETH price from the influence of the BTC price
        eth_price -= 0.05 * btc_price

        return eth_price

    def monitor_price(self, threshold):
        while True:
            # Wait for 1 second
            time.sleep(1)

            # Get the latest price of the BETHESDA futures
            price = self.get_eth_price()

            # Check if this is the first iteration of the loop
            if self.prev_price is not None:
                # Calculate the percentage change in the price over the last 60 minutes
                percent_change = (price - self.prev_price) / self.prev_price * 100

                # Check if the percentage change is greater than the threshold
                if abs(percent_change) > threshold:
                    print(f"Price change: {percent_change:.2f}%")

            # Update the previous price
            self.prev_price = price


if __name__ == '__main__':
    # Enter your API keys here
    api_key = ''
    api_secret = ''

    # Set the symbol for the BETHESDA futures
    symbol = 'BETHESDAUSDT'

    # Set the threshold for price changes
    threshold = 1

    # Initialize the price monitor
    monitor = PriceMonitor(api_key, api_secret, symbol)

    # Start monitoring the price
    monitor.monitor_price(threshold)
