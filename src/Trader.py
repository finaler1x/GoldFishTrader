def init_broker_connection():
    return "test"


def create_order(trading_client, ticker):
    pass


def execute_trade(ticker1, ticker2):
    client = init_broker_connection()
    create_order(client, ticker1)
    create_order(client, ticker2)

    print("Execute trade.")
