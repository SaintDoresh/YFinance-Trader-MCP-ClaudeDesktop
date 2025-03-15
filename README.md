# YFinance Trader MCP Tool for Claude Desktop

An MCP (Model Context Protocol) tool that provides stock market data and trading capabilities using the yfinance library, specifically adapted for Claude Desktop.

> **Credit**: This project was inspired by [mcp-stocks](https://github.com/luigiajah/mcp-stocks) by Luigi Ajah, which is a similar implementation for Cursor. This adaptation modifies the original concept to work with Claude Desktop.

## Features

- Real-time stock quotes
- Company information and financial metrics
- Historical price data
- Symbol search functionality
- Analyst recommendations
- Insider transaction tracking

## Setup

1. Ensure you have Python 3.10 or higher installed

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Integration with Claude Desktop

1. Configure your MCP settings in Claude Desktop by adding the following to your MCP configuration:

```json
{
  "mcpServers": {
    "yfinance-trader": {
      "command": "py",
      "args": ["-3.13", "path/to/your/main.py"]
    }
  }
}
```

2. Replace the path with the full path to your main.py file
3. Restart Claude Desktop if needed

## Available Tools

### 1. get_stock_quote
Get real-time stock quote information:
```json
{
    "symbol": "AAPL",
    "price": 150.25,
    "change": 2.5,
    "changePercent": 1.67,
    "volume": 1234567,
    "timestamp": "2024-03-20T10:30:00"
}
```

### 2. get_company_overview
Get company information and key metrics:
```json
{
    "name": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "marketCap": 2500000000000,
    "peRatio": 25.4,
    "forwardPE": 24.2,
    "dividendYield": 0.65,
    "52WeekHigh": 182.94,
    "52WeekLow": 124.17
}
```

### 3. get_time_series_daily
Get historical daily price data:
```json
{
    "symbol": "AAPL",
    "timeSeriesDaily": [
        {
            "date": "2024-03-20T00:00:00",
            "open": 150.25,
            "high": 152.30,
            "low": 149.80,
            "close": 151.75,
            "volume": 12345678
        }
        // ... more data points
    ]
}
```

### 4. search_symbol
Search for stocks and other securities:
```json
{
    "results": [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "type": "EQUITY",
            "exchange": "NASDAQ"
        }
        // ... more results
    ]
}
```

### 5. get_recommendations
Get analyst recommendations for a stock:
```json
{
    "symbol": "AAPL",
    "recommendations": [
        {
            "period": "2024-03-15T00:00:00",
            "strongBuy": 15,
            "buy": 20,
            "hold": 8,
            "sell": 2,
            "strongSell": 0
        }
        // ... more periods
    ]
}
```

### 6. get_insider_transactions
Get insider trading information:
```json
{
    "symbol": "AAPL",
    "transactions": [
        {
            "date": "2024-03-15T00:00:00",
            "insider": "John Doe",
            "position": "Director",
            "transactionType": "Buy",
            "shares": 1000,
            "value": 150250.00,
            "url": "https://finance.yahoo.com/...",
            "text": "Purchase of 1000 shares",
            "startDate": "2024-03-15",
            "ownership": "Direct"
        }
        // ... more transactions
    ]
}
```

## Sample Queries

You can ask Claude Desktop questions like:
- "What is the current stock price and daily change for AAPL?"
- "Can you give me a company overview for Microsoft (MSFT)?"
- "Show me the historical price data for Tesla (TSLA) over the last 3 months."
- "Search for stocks related to 'NVDA'."
- "What are the analyst recommendations for Amazon (AMZN)?"
- "Have there been any recent insider transactions for Google (GOOGL)?"

## Cryptocurrency Support

Limited cryptocurrency data is available using special ticker formats:
- BTC-USD for Bitcoin
- ETH-USD for Ethereum
- DOGE-USD for Dogecoin

## Error Handling

All tools include proper error handling and will return an error message if something goes wrong:
```json
{
    "error": "Failed to fetch quote for INVALID_SYMBOL"
}
```

## Troubleshooting

If the MCP server is not working in Claude Desktop:
1. Make sure the server is running - you should see output when you start the script
2. Verify the path in your settings is correct and absolute
3. Make sure Python 3.10+ is in your system PATH
4. Check that all dependencies are installed
5. Try restarting Claude Desktop
6. Check logs for any error messages

## Differences from the original mcp-stocks project

- Uses the MCP library directly instead of FastAPI
- Adapted for Claude Desktop instead of Cursor
- Modified error handling and response formats
- Updated configuration approach

## License

MIT License
