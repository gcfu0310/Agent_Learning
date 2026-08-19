from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv
load_dotenv()

"""
将向量检索加入langchain的链中
"""
# 对话提示词
Chat_Prompt = ChatPromptTemplate.from_messages(
    [
        ("system","以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
        ("human","用户提问：{input}")
    ]
)

# 向量模型
embedding_model = OpenAIEmbeddings(
    model=os.getenv("embedding_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url"),
    check_embedding_ctx_length=False
)

# 大语言模型
llm_model = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)

# 内存向量存储库
vectorstores = InMemoryVectorStore(embedding=embedding_model)

# 向内存向量存储库添加数据
vectorstores.add_texts(["减肥就是要少吃多练", "在减脂期间吃东西很重要,清淡少油控制卡路里摄入并运动起来", "跑步是很好的运动哦"])

# 用户提问内容
query = "怎么减肥？"

# 将向量检索入链,返回的是Runnable接口的子类，只有Runnable接口的子类才能入链
retriever = vectorstores.as_retriever(search_kwargs={"k":2})

# 输出函数
def format_func(result: list[Document]) -> str:
    context = "["
    for res in result:
        context += res.page_content
        context += ";"
    context += "]"
    return context

# 解析器
str_parser = StrOutputParser()

# 打印完整prompt的函数
def print_Prompt(prompt):
    print("="*20,prompt.to_string(),"="*20)
    return prompt

# 构建链
"""
retriever:
    - 输入：用户的提问       str
    - 输出：向量库的检索结果  list[Document]
prompt:
    - 输入：用户的提问 + 向量库的检索结果   dict
    - 输出：完整的提示词                 PromptValue
"""
chain = {"input":RunnablePassthrough(),"context": retriever|format_func}|Chat_Prompt|print_Prompt|llm_model|str_parser

res = chain.invoke(input=query)
print(res)
