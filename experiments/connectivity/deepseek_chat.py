import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
    model="deepseek-chat",
    openai_api_base="https://api.deepseek.com/v1"
)

response = llm("你好")
print(response)
