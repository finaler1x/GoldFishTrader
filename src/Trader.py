from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from config import configs


def init_broker_connection():
    # test mode ON
    broker_config = configs.secret.alpaca.sandbox

    return TradingClient(broker_config.api_key, broker_config.api_secret, paper=True)


def create_order(trading_client, ticker):

    # preparing orders
    market_order_data = MarketOrderRequest(
        symbol=ticker,
        qty=0.023,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY
    )

    # Market order
    market_order = trading_client.submit_order(
        order_data=market_order_data
    )


def execute_trade(ticker):
    client = init_broker_connection()
    create_order(client, ticker)

    print("Execute trade.")
