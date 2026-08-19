from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
load_dotenv()

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

# 向量检索后的top-k结果
result = vectorstores.similarity_search(query=query,k=2)

# 将结果整理成str类型
context = "["
for res in result:
    context += res.page_content
    context += ";"
context += "]"

# 构建链
str_parser = StrOutputParser()

def print_Prompt(prompt):
    print("="*20,prompt.to_string(),"="*20)
    return prompt

chain = Chat_Prompt|print_Prompt|llm_model|str_parser

res = chain.invoke(input={"context":context,"input":query})
print(res)
