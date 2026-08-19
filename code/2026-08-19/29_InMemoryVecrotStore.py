from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()

# 定义一个嵌入模型
embedding_model = OpenAIEmbeddings(
    model=os.getenv("embedding_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url"),
    check_embedding_ctx_length=False
)

# 定义一个内存向量存储器
vector_stores = InMemoryVectorStore(
    embedding=embedding_model # 将文本转为向量的嵌入模型
)

# 读取文件
csv_loader = CSVLoader(
    file_path="D:/Agent-Learning/code/2026-08-19/data/info.csv",
    source_column="source",
    encoding="utf-8"
)

# 生成[Document,Document...]
documents = csv_loader.load()
# print(documents)

# 内存向量存储器添加向量文件
vector_stores.add_documents(
    documents=documents,  # 已经是[Doucment]格式的文本文件
    ids=["id"+str(i) for i in range(1,len(documents)+1)] # 对应的id编号
)

# 内存向量存储器删除向量文件
vector_stores.delete(
    ids=["id1","id2"]    # 删除指定id的向量文件
)

# 计算内存向量存储器里的向量与query的相似度,返回[Document,Document...]
result = vector_stores.similarity_search(
    query="python是不是简单易学",
    k=3
)
print(result)
