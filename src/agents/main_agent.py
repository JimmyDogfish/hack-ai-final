# Import necessary modules and classes
from uagents import Agent, Bureau, Context, Model
import pandas as pd
from uagents.setup import fund_agent_if_low
import requests
from config import api_key

# Set the address of the AI model agent
AI_MODEL_AGENT_ADDRESS = "agent1q05wcd5zddcre8lxelmq8zuftxm4ngpe3ehmagwxmth6zrcfvpe8vcl9rc0"

# Define a model class for symbol
class Symbol(Model):
    text: str

#Define a advice class
class Advice(Model):
    text: str

# Get user input for the desired company name
company_name = input("Enter the name of the desired company: ")

# Build the URL to retrieve company data based on the provided company name
ticker_complete_url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=' + company_name + '&apikey=' + api_key

# Make a request to the Alpha Vantage API to get company data in JSON format
company_data_json = requests.get(ticker_complete_url)
company_data = company_data_json.json()

# Function to extract relevant fields from the retrieved data
def extract_fields(data):
    extracted_data = []
    for entry in data['bestMatches']:
        extracted_entry = {
            'Name': entry.get('2. name', ''),
            'Symbol': entry.get('1. symbol', ''),
            'Region': entry.get('4. region', ''),
            'Currency': entry.get('8. currency', '')
        }
        extracted_data.append(extracted_entry)
    return extracted_data

# Extract relevant fields from the company data
extracted_data = extract_fields(company_data)

# Create a pandas DataFrame from the extracted data
df = pd.DataFrame(extracted_data)

# Print the DataFrame
print(df)

# Get user input for the symbol of the desired company
company_symbol = input("Enter the symbol of the desired company: ")

# Create an instance of the Agent class
agent = Agent(name="alice", seed="alice recovery phrase", port=8000, endpoint=["http://127.0.0.1:8000/submit"])

# Fund the agent if the wallet balance is low
fund_agent_if_low(agent.wallet.address())

# Define an interval function to send the symbol to the ML agent
@agent.on_interval(300)
async def send_symbol(ctx: Context):
    ctx.logger.info(f"Sending symbol to the ML agent: {company_symbol}")
    await ctx.send(AI_MODEL_AGENT_ADDRESS, Symbol(text=company_symbol))

@agent.on_message(model=Advice)
async def handle_message(ctx: Context, sender: str, data: Model):
    ctx.logger.info(f"{data.text}")

# Run the agent if the script is executed as the main module
if __name__ == "__main__":
    agent.run()
