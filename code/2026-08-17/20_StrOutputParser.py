from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

prompt_text = PromptTemplate.from_template(
    "我的邻居姓{last_name},有一个刚出生的{gender},取一个名字"
)
llm = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)
# StrOutputParser可以把AIMessage类转换成str
parser = StrOutputParser()
chain = prompt_text | llm | parser | llm
# chain = prompt_text | llm | parser | llm | parser
res = chain.invoke({"last_name":"付","gender":"女儿"})
print(res.content)
# print(res)