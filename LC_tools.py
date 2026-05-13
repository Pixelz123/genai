from langchain_core.tools import tool,StructuredTool,BaseTool
from typing import Type
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

import os 
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING"]=os.getenv("LANGSMITH_TRACING")


# @tool
# def multiply(a: float, b: float) -> float:
#     """Multiplies two numbers together."""
#     return a * b
# res= multiply.invoke({"a": 3, "b": 4})
# print(res)
# print(multiply.name)
# print(multiply.description)
# print(multiply.args_schema.model_json_schema())
class MultiplyArgs(BaseModel):
    a: float = Field(..., description="The first number to multiply.")
    b: float = Field(..., description="The second number to multiply.")
# def multiply(a, b) -> float:
#     """Multiplies two numbers together."""
#     return a * b
# multiply_tool = StructuredTool.from_function(
#     func=multiply,
#     name="multiply",
#     description="Multiplies two numbers together.",
#     args_schema=MultiplyArgs
#     )
# res= multiply_tool.invoke({"a": 3, "b": 4})
# print(res) 
class MultiplyTool(BaseTool):
    name: str = "multiply2"
    description: str = "Multiplies two numbers together."
    args_schema: Type[BaseModel] = MultiplyArgs
    def _run(self, a: float, b: float) -> float:
        return a * b
multiply_tool2 = MultiplyTool()
res2= multiply_tool2.invoke({"a": 3, "b": 4})
# print(res2)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
llm= llm.bind_tools([multiply_tool2])
response = llm.invoke("can you multiply 3 with 10 ")
print(response)