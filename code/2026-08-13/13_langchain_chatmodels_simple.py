from langchain_openai.chat_models import ChatOpenAI
from langchain_ollama.chat_models import ChatOllama
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"), 
    base_url = os.getenv("base_url")
)
messages = [
    ("system","你是一名边塞诗人"),
    ("human","写一首诗"),
    ("ai","塞上风沙卷战袍，孤城遥对月轮高。黄云压阵千军寂，铁马嘶寒万骨凋。胡笳声断长城外，羌笛愁生大漠皋。莫道书生无胆气，一腔热血染征刀。"),
    ("human","基于上述内容，写一首七言律诗")
]
for chunk in llm.stream(messages):
    print(chunk.content,end='',flush=True)

o_llm = ChatOllama(
    model="qwen2.5:7b"
)
messages = [
    ("system","你是一名边塞诗人"),
    ("human","写一首诗"),
    ("ai","塞上风沙卷战袍，孤城遥对月轮高。黄云压阵千军寂，铁马嘶寒万骨凋。胡笳声断长城外，羌笛愁生大漠皋。莫道书生无胆气，一腔热血染征刀。"),
    ("human","基于上述内容，写一首七言律诗")
]
for chunk in o_llm.stream(messages):
    print(chunk.content,end='',flush=True)