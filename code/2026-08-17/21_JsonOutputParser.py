from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

first_prompt = PromptTemplate.from_template(
    "我的邻居姓{last_name},生了一个{gender},起一个名字，并封装成json格式返回"
    "key为name,value就是你取的名字，严格按照格式要求返回"
)
second_prompt = PromptTemplate.from_template(
    "姓名{name},请解析这个名字的含义"
)
str_parser = StrOutputParser()
json_parser = JsonOutputParser()
llm = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)
chain = first_prompt|llm|json_parser|second_prompt|llm|str_parser
for chunk in chain.stream({"last_name":"付","gender":"女儿"}):
    print(chunk,end='',flush=True)