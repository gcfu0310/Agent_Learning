from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
import os
from dotenv import load_dotenv
load_dotenv()

# 调用服务器的LLMs
llm = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)
res = llm.invoke("讲一个超级好笑的笑话逗笑我")
print(res.content)

# 调用本地的模型
# O_llm = OllamaLLM(
#     model="qwen2.5:7b"
# )
# res = O_llm.invoke("讲一个谐音梗笑话")
# print(res)