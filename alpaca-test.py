

import os
from datetime import datetime
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
# Load environment variables from .env file
load_dotenv()

# Get environment variables
api_key = os.getenv('ALPACA_API_KEY_ID')
secret_key = os.getenv('ALPACA_API_SECRET_KEY')
base_url = os.getenv('ALPACA_API_BASE_URL')

trading_client = TradingClient(
    api_key=api_key,
    secret_key=secret_key
)

limit_order_data = LimitOrderRequest(
    symbol="SPY",
    qty=1,
    side=OrderSide.BUY,
    time_in_force=TimeInForce.DAY,
    limit_price=450.00
)

market_order = trading_client.submit_order(limit_order_data)
print(market_order)