from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(
    model="qwen-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)
res = llm.stream("简单介绍一下电子科技大学")
for chunk in res:
    print(chunk.content,end='',flush=True)

print("\n========================================================")
o_llm = OllamaLLM(
    model="qwen2.5:7b"
)
res = o_llm.stream("简单评价一下电子科技大学")
for chunk in res:
    print(chunk,end='',flush=True)