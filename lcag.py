from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_community.tools import GoogleSearchRun
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
os.environ["GOOGLE_CSE_ID"] = os.getenv("GOOGLE_CSE_ID", "")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING", "")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

search_api = GoogleSearchAPIWrapper()
search_tool = GoogleSearchRun(api_wrapper=search_api)

tools = [search_tool]
prompt = "You are a helpful assistant that answers questions by using the available tools."
agent = create_agent(llm, tools, system_prompt=prompt)

question = "What is the current stock price of Google?"
response = agent.invoke(question)
print(response)
