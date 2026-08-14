from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)
prompt_template = PromptTemplate.from_template("我的邻居姓{last_name}，他生了一个{gender}，给他的女儿取一个名字，简短回答")
prompt_text = prompt_template.format(last_name="熊",gender="女儿")
# res = model.invoke(input=prompt_text)
# print(res.content)

# 为什么使用PromptTemplate这个类对象而不是字符串作为prompt，请看以下代码：
# 1、PromptTemplate类，支持langchain的框架的链式调用
# 2、在大型工程中更容易标准化
chain = prompt_template | model
res = chain.invoke(input={"last_name":"付","gender":"女儿"})
print(res.content)