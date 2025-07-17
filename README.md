# Alpaca Stock Trading Bot

A simple, user-friendly command-line chatbot for stock trading using the Alpaca API. This bot allows you to check market prices, buy and sell stocks, place limit orders, and view your portfolio and account information.

## Features

- Check your account balance and portfolio value
- Get real-time stock prices
- Buy and sell stocks at market price
- Place limit orders with custom prices
- View your current portfolio with profit/loss information
- Paper trading support (practice with virtual money)

## Prerequisites

- Python 3.6+
- Alpaca API account (free tier available)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/alpaca-stock-trading-bot.git
cd alpaca-stock-trading-bot
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Alpaca API credentials:
```
ALPACA_API_BASE_URL = https://paper-api.alpaca.markets/v2
ALPACA_API_KEY_ID = YOUR_API_KEY
ALPACA_API_SECRET_KEY = YOUR_SECRET_KEY
```

Note: The default URL is for paper trading (simulation). For real trading, use `https://api.alpaca.markets/v2`.

## Usage

Run the chatbot:
```bash
python trading_chatbot.py
```

### Available Commands

- `account` - View your account information
- `price [symbol]` - Get current price of a stock (e.g., `price AAPL`)
- `buy [symbol] [quantity]` - Buy stock at market price (e.g., `buy MSFT 5`)
- `sell [symbol] [quantity]` - Sell stock at market price (e.g., `sell TSLA 2`)
- `buy limit [symbol] [quantity] [price]` - Place a limit buy order (e.g., `buy limit AMZN 1 3500.00`)
- `sell limit [symbol] [quantity] [price]` - Place a limit sell order (e.g., `sell limit GOOGL 3 2800.50`)
- `portfolio` - View your current portfolio
- `help` - Display available commands
- `exit` - Exit the chatbot

## Security

- Never commit your `.env` file with API keys to version control
- This project uses the `.gitignore` file to prevent sensitive information from being shared



## Disclaimer

This tool is for educational and informational purposes only. It is not intended to provide investment advice. Always do your own research and consider seeking advice from a licensed financial professional before making investment decisions. Trading stocks involves risk, and you may lose money.
