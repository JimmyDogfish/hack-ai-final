# Import necessary modules and classes
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.fundamentaldata import FundamentalData
from config import api_key

# Define a model class for symbol
class Symbol(Model):
    text: str

class Advice(Model):
    text: str

# Create an instance of the Agent class for the ML agent
ml_agent = Agent(name="ml_agent", seed="ml_agent recovery phrase", port=8001, endpoint=["http://127.0.0.1:8001/submit"])

# Fund the agent if the wallet balance is low
fund_agent_if_low(ml_agent.wallet.address())

# Define a message handling function for the Symbol model
@ml_agent.on_message(model=Symbol)
async def handle_data(ctx: Context, sender: str, data: Symbol):
    ctx.logger.info(f"Got response from AI model agent: {data}")
    symbol = data.text

    # Initialize Alpha Vantage API clients
    ts = TimeSeries(key=api_key, output_format='pandas')
    ti = TechIndicators(key=api_key, output_format='pandas')
    fd = FundamentalData(key=api_key, output_format='pandas')

    # Step 1: Get historical stock prices
    historical_data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
    print("\nHistorical Stock Prices:")
    print(historical_data.head())

    # Step 2: Get technical indicators
    technical_indicators, meta_data = ti.get_sma(symbol=symbol)
    print("\nTechnical Indicators (SMA):")
    print(technical_indicators.head())

    # Step 3: Get company overview
    company_overview, meta_data = fd.get_company_overview(symbol=symbol)
    print("\nCompany Overview:")
    print(company_overview)

    # Get historical stock prices
    historical_data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')

    # Calculate percentage change
    historical_data['Daily Return'] = historical_data['4. close'].pct_change() * 100

    # Check if the most recent daily return is positive, negative, or unchanged
    recent_return = historical_data['Daily Return'].iloc[-1]
    if recent_return > 0:
        await ctx.send(sender, Advice(text=f"Investing in {symbol} is currently profitable."))
    elif recent_return < 0:
        await ctx.send(sender, Advice(text=f"Investing in {symbol} is currently not profitable."))
    else:
        await ctx.send(sender, Advice(text=f"The stock {symbol} has no recent change in value."))

# Run the ML agent if the script is executed as the main module
if __name__ == "__main__":
    ml_agent.run()
