import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import datetime

# Load environment variables from .env file
load_dotenv()

# Get environment variables
api_key = os.getenv('ALPACA_API_KEY_ID')
secret_key = os.getenv('ALPACA_API_SECRET_KEY')
base_url = os.getenv('ALPACA_API_BASE_URL')

# Initialize clients
trading_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=True)
stock_client = StockHistoricalDataClient(api_key=api_key, secret_key=secret_key)

def get_account_info():
    """Get account information"""
    account = trading_client.get_account()
    return f"Account Information:\n" \
           f"- Cash Balance: ${float(account.cash):.2f}\n" \
           f"- Portfolio Value: ${float(account.portfolio_value):.2f}\n" \
           f"- Buying Power: ${float(account.buying_power):.2f}"

def get_stock_price(symbol):
    """Get current stock price"""
    # Get today's bars
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=5)  # Using a 5-day range to ensure we get data

    request_params = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame.DAY,
        start=yesterday.date(),
        end=today.date()
    )
    
    try:
        bars = stock_client.get_stock_bars(request_params)
        if symbol in bars.data:
            latest_bar = bars.data[symbol][-1]
            return f"Latest price for {symbol}: ${latest_bar.close:.2f}"
        else:
            return f"No data found for {symbol}"
    except Exception as e:
        return f"Error getting price for {symbol}: {str(e)}"

def buy_stock_market(symbol, qty):
    """Buy stock at market price"""
    order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY
    )
    
    try:
        order = trading_client.submit_order(order_data)
        return f"Market order to buy {qty} shares of {symbol} submitted successfully!"
    except Exception as e:
        return f"Error placing buy order: {str(e)}"

def sell_stock_market(symbol, qty):
    """Sell stock at market price"""
    order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.DAY
    )
    
    try:
        order = trading_client.submit_order(order_data)
        return f"Market order to sell {qty} shares of {symbol} submitted successfully!"
    except Exception as e:
        return f"Error placing sell order: {str(e)}"

def buy_stock_limit(symbol, qty, price):
    """Buy stock with limit order"""
    order_data = LimitOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
        limit_price=price
    )
    
    try:
        order = trading_client.submit_order(order_data)
        return f"Limit order to buy {qty} shares of {symbol} at ${price:.2f} submitted successfully!"
    except Exception as e:
        return f"Error placing limit buy order: {str(e)}"

def sell_stock_limit(symbol, qty, price):
    """Sell stock with limit order"""
    order_data = LimitOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
        limit_price=price
    )
    
    try:
        order = trading_client.submit_order(order_data)
        return f"Limit order to sell {qty} shares of {symbol} at ${price:.2f} submitted successfully!"
    except Exception as e:
        return f"Error placing limit sell order: {str(e)}"

def get_portfolio():
    """Get current portfolio positions"""
    positions = trading_client.get_all_positions()
    if not positions:
        return "You don't have any open positions."
    
    result = "Your Portfolio:\n"
    for position in positions:
        market_value = float(position.market_value)
        cost_basis = float(position.cost_basis)
        profit_loss = market_value - cost_basis
        profit_loss_percent = (profit_loss / cost_basis) * 100 if cost_basis != 0 else 0
        
        result += f"- {position.symbol}: {position.qty} shares\n"
        result += f"  Current Value: ${market_value:.2f}\n"
        result += f"  Profit/Loss: ${profit_loss:.2f} ({profit_loss_percent:.2f}%)\n"
    
    return result

def display_help():
    """Display available commands"""
    return """
Available Commands:
------------------
account - View your account information
price [symbol] - Get current price of a stock
buy [symbol] [quantity] - Buy stock at market price
sell [symbol] [quantity] - Sell stock at market price
buy limit [symbol] [quantity] [price] - Place a limit buy order
sell limit [symbol] [quantity] [price] - Place a limit sell order
portfolio - View your current portfolio
help - Display this help message
exit - Exit the chatbot
"""

def chatbot():
    print("=== Alpaca Trading Chatbot ===")
    print("Type 'help' to see available commands or 'exit' to quit.")
    
    while True:
        try:
            user_input = input("\nWhat would you like to do? ").strip().lower()
            
            if user_input == "exit":
                print("Thank you for using Alpaca Trading Chatbot. Goodbye!")
                break
                
            elif user_input == "help":
                print(display_help())
                
            elif user_input == "account":
                print(get_account_info())
                
            elif user_input == "portfolio":
                print(get_portfolio())
                
            elif user_input.startswith("price "):
                _, symbol = user_input.split(" ", 1)
                print(get_stock_price(symbol.upper()))
                
            elif user_input.startswith("buy limit "):
                parts = user_input.split(" ")
                if len(parts) >= 5:  # "buy limit TSLA 2 900.50"
                    symbol = parts[2]
                    qty = parts[3]
                    price = parts[4]
                    print(buy_stock_limit(symbol.upper(), float(qty), float(price)))
                else:
                    print("Invalid format. Use: buy limit [symbol] [quantity] [price]")
                    
            elif user_input.startswith("sell limit "):
                parts = user_input.split(" ")
                if len(parts) >= 5:  # "sell limit TSLA 2 900.50"
                    symbol = parts[2]
                    qty = parts[3]
                    price = parts[4]
                    print(sell_stock_limit(symbol.upper(), float(qty), float(price)))
                else:
                    print("Invalid format. Use: sell limit [symbol] [quantity] [price]")
                    
            elif user_input.startswith("buy "):
                _, symbol, qty = user_input.split(" ", 2)
                print(buy_stock_market(symbol.upper(), float(qty)))
                
            elif user_input.startswith("sell "):
                _, symbol, qty = user_input.split(" ", 2)
                print(sell_stock_market(symbol.upper(), float(qty)))
                
            else:
                print("I don't understand that command. Type 'help' to see available options.")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please try again or type 'help' for assistance.")

if __name__ == "__main__":
    chatbot()
