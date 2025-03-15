from typing import Any, Dict, List
import yfinance as yf
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("yfinance-trader")

@mcp.tool("get_stock_quote")
async def get_stock_quote(symbol: str) -> Dict[str, Any]:
    """Get real-time stock quote information.
    
    Args:
        symbol (str): Stock symbol (e.g., AAPL, MSFT, GOOGL)
    
    Returns:
        Dict containing current stock price and related information
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "symbol": symbol,
            "price": info.get("regularMarketPrice", 0),
            "change": info.get("regularMarketChange", 0),
            "changePercent": info.get("regularMarketChangePercent", 0),
            "volume": info.get("regularMarketVolume", 0),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching quote for {symbol}: {str(e)}")
        return {"error": f"Failed to fetch quote for {symbol}"}

@mcp.tool("get_company_overview")
async def get_company_overview(symbol: str) -> Dict[str, Any]:
    """Get company information, financial ratios, and other key metrics.
    
    Args:
        symbol (str): Stock symbol (e.g., AAPL, MSFT, GOOGL)
    
    Returns:
        Dict containing company information and key metrics
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "name": info.get("longName", ""),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
            "marketCap": info.get("marketCap", 0),
            "peRatio": info.get("trailingPE", 0),
            "forwardPE": info.get("forwardPE", 0),
            "dividendYield": info.get("dividendYield", 0),
            "52WeekHigh": info.get("fiftyTwoWeekHigh", 0),
            "52WeekLow": info.get("fiftyTwoWeekLow", 0)
        }
    except Exception as e:
        logger.error(f"Error fetching company overview for {symbol}: {str(e)}")
        return {"error": f"Failed to fetch company overview for {symbol}"}

@mcp.tool("get_time_series_daily")
async def get_time_series_daily(symbol: str, outputsize: str = "compact") -> Dict[str, Any]:
    """Get daily time series stock data.
    
    Args:
        symbol (str): Stock symbol (e.g., AAPL, MSFT, GOOGL)
        outputsize (str): Output size: 'compact' (latest 100 data points) or 'full' (up to 20 years of data)
    
    Returns:
        Dict containing historical daily price data
    """
    try:
        stock = yf.Ticker(symbol)
        period = "3mo" if outputsize == "compact" else "max"
        history = stock.history(period=period)
        
        data = []
        for date, row in history.iterrows():
            data.append({
                "date": date.isoformat(),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
                "volume": row["Volume"]
            })
        
        return {
            "symbol": symbol,
            "timeSeriesDaily": data
        }
    except Exception as e:
        logger.error(f"Error fetching time series for {symbol}: {str(e)}")
        return {"error": f"Failed to fetch time series for {symbol}"}

@mcp.tool("search_symbol")
async def search_symbol(keywords: str) -> Dict[str, Any]:
    """Search for stocks, ETFs, mutual funds, or other securities.
    
    Args:
        keywords (str): Keywords to search for (e.g., apple, microsoft, tech)
    
    Returns:
        Dict containing search results
    """
    try:
        tickers = yf.Tickers(keywords)
        results = []
        
        for symbol in keywords.split():
            try:
                info = tickers.tickers[symbol].info
                results.append({
                    "symbol": symbol,
                    "name": info.get("longName", ""),
                    "type": info.get("quoteType", ""),
                    "exchange": info.get("exchange", "")
                })
            except:
                continue
                
        return {"results": results}
    except Exception as e:
        logger.error(f"Error searching for {keywords}: {str(e)}")
        return {"error": f"Failed to search for {keywords}"}

@mcp.tool("get_recommendations")
async def get_recommendations(symbol: str) -> Dict[str, Any]:
    """Get analyst recommendations for a stock.
    
    Args:
        symbol (str): Stock symbol (e.g., AAPL, MSFT, GOOGL)
    
    Returns:
        Dict containing analyst recommendations including strongBuy, buy, hold, sell, strongSell counts
    """
    try:
        stock = yf.Ticker(symbol)
        recommendations = stock.recommendations
        
        if recommendations is None or recommendations.empty:
            return {
                "symbol": symbol,
                "recommendations": []
            }
            
        # Convert the recommendations DataFrame to a list of dictionaries
        recs = []
        for index, row in recommendations.iterrows():
            rec_data = {
                "period": index.isoformat() if hasattr(index, "isoformat") else str(index),
                "strongBuy": int(row.get("strongBuy", 0)),
                "buy": int(row.get("buy", 0)),
                "hold": int(row.get("hold", 0)),
                "sell": int(row.get("sell", 0)),
                "strongSell": int(row.get("strongSell", 0))
            }
            recs.append(rec_data)
            
        return {
            "symbol": symbol,
            "recommendations": recs
        }
    except Exception as e:
        logger.error(f"Error fetching recommendations for {symbol}: {str(e)}")
        return {"error": f"Failed to fetch recommendations for {symbol}"}

@mcp.tool("get_insider_transactions")
async def get_insider_transactions(symbol: str) -> Dict[str, Any]:
    """Get insider transactions for a company.
    
    Args:
        symbol (str): Stock symbol (e.g., AAPL, MSFT, GOOGL)
    
    Returns:
        Dict containing recent insider transactions
    """
    try:
        stock = yf.Ticker(symbol)
        insider = stock.insider_transactions
        
        if insider is None or insider.empty:
            return {
                "symbol": symbol,
                "transactions": []
            }
            
        transactions = []
        for index, row in insider.iterrows():
            transaction = {
                "date": index.isoformat() if hasattr(index, "isoformat") else str(index),
                "insider": row.get("Insider", ""),
                "position": row.get("Position", ""),
                "transactionType": row.get("Transaction", ""),
                "shares": int(row.get("Shares", 0)),
                "value": float(row.get("Value", 0)),
                "url": row.get("URL", ""),
                "text": row.get("Text", ""),
                "startDate": row.get("Start Date", ""),
                "ownership": row.get("Ownership", "")
            }
            transactions.append(transaction)
            
        return {
            "symbol": symbol,
            "transactions": transactions
        }
    except Exception as e:
        logger.error(f"Error fetching insider transactions for {symbol}: {str(e)}")
        return {"error": f"Failed to fetch insider transactions for {symbol}"}

if __name__ == "__main__":
    mcp.run()