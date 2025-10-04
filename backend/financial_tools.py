import yfinance as yf
import requests

def get_ticker_symbol(company_name: str) -> str:
    """Uses an open API to find the best ticker symbol for a company name."""
    yfinance_url = f"https://query2.finance.yahoo.com/v1/finance/search?q={company_name}"
    headers = {'User-Agent': 'Mozilla/5.0'} # Yahoo requires a user-agent header
    response = requests.get(yfinance_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('quotes'):
            return data['quotes'][0]['symbol']
    return None

def get_company_analysis(company_name: str) -> dict:
    """
    Fetches financial data for a company, calculates key metrics, and returns them.
    """
    print(f"Finding ticker for {company_name}...")
    ticker_symbol = get_ticker_symbol(company_name)
    if not ticker_symbol:
        return {"error": f"Could not find a stock ticker for '{company_name}'."}
    
    print(f"Fetching data for ticker {ticker_symbol}...")
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    # 1. Fetch Key Data Points
    # We use .get() to avoid errors if a data point is missing
    market_cap = info.get('marketCap', 0)
    total_debt = info.get('totalDebt', 0)
    beta = info.get('beta', 1.0) # Assume 1.0 (market risk) if not available
    free_cash_flow = info.get('freeCashflow', 0)
    shares_outstanding = info.get('sharesOutstanding', 0)
    
    if market_cap == 0 or shares_outstanding == 0:
         return {"error": f"Could not fetch essential data like Market Cap for {ticker_symbol}."}

    # 2. Perform Simplified Calculations
    # These are simplified for the prototype but follow the standard logic.
    
    # Simplified WACC (Weighted Average Cost of Capital)
    cost_of_equity = 0.05 + beta * (0.08 - 0.05) # RiskFreeRate + Beta * (MarketReturn - RiskFreeRate)
    cost_of_debt = 0.05 # Assumed average interest rate on debt
    tax_rate = 0.25 # Assumed corporate tax rate
    
    equity_weight = market_cap / (market_cap + total_debt)
    debt_weight = total_debt / (market_cap + total_debt)
    
    wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))

    # Simplified DCF (Discounted Cash Flow) Valuation
    # Project cash flow for 5 years with a 3% growth rate, then find terminal value
    growth_rate = 0.03
    discount_rate = wacc
    
    projected_cash_flows = [free_cash_flow * (1 + growth_rate) ** i for i in range(1, 6)]
    
    # Terminal value using Gordon Growth Model
    terminal_value = (projected_cash_flows[-1] * (1 + growth_rate)) / (discount_rate - growth_rate)
    
    # Discount all future cash flows back to today's value
    dcf_value = sum([cf / (1 + discount_rate) ** i for i, cf in enumerate(projected_cash_flows, 1)])
    dcf_value += terminal_value / (1 + discount_rate) ** 5
    
    dcf_per_share = dcf_value / shares_outstanding if shares_outstanding else 0

    return {
        "ticker_symbol": ticker_symbol,
        "market_cap": market_cap,
        "total_debt": total_debt,
        "beta": beta,
        "wacc": round(wacc * 100, 2), # Return as a percentage
        "dcf_per_share_value": round(dcf_per_share, 2),
        "current_price": info.get('currentPrice', 'N/A')
    }