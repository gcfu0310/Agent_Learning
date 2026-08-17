from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

first_prompt = PromptTemplate.from_template(
    "我姓{last_name},生了一个{gender}，请取个名字，仅回答我名字即可"
)
second_prompt = PromptTemplate.from_template(
    "{name}请解析这个名字的含义"
)
str_parser = StrOutputParser()
my_func = RunnableLambda(lambda ai_mes:{"name":"ai_mes.content"})
llm = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)
chain = first_prompt|llm|my_func|second_prompt|llm|str_parser
for chunk in chain.stream(input={"last_name":"杨","gender":"女儿"}):
    print(chunk,end='',flush=True)