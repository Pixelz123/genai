from typing import Annotated

from langchain_core.tools import InjectedToolArg, tool
from langchain_google_genai import ChatGoogleGenerativeAI
import requests

import os 
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING"]=os.getenv("LANGSMITH_TRACING")

@tool 
def get_conversion_rate(base_currency: str , target_currency: str)-> float:
    """This tool gets the conversion factor between a given base currency to a target currency"""
    url = f"https://v6.exchangerate-api.com/v6/ef5943d4ceef6ac160bdbd75/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    return response.json()["conversion_rate"]

@tool
def convert_currency(base_currency_value: float, conversion_rate: float)-> float:
    """This tool converts a given value in base currency to target currency using the conversion rate"""
    return base_currency_value * conversion_rate


message = ["What is the conversion factor from USD to INR and based on that can you convert 10 USD to INR ? "]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
llm_with_tools= llm.bind_tools([get_conversion_rate, convert_currency])
response = llm_with_tools.invoke("What is the conversion factor from USD to INR and based on that can you convert 10 USD to INR ? ")
print(response.tool_calls)

# Map tools by their names for easy lookup
tools_map = {tool.name: tool for tool in [get_conversion_rate, convert_currency]}
print(response.tool_calls[0]['args'])
for tool_call in response.tool_calls:
    selected_tool = tools_map.get(tool_call["name"])
    if selected_tool:
        result = selected_tool.invoke(tool_call["args"])
        print(f"Result from {tool_call['name']}: {result}")