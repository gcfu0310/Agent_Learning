from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
import os
from dotenv import load_dotenv
load_dotenv()

embedding_model = OpenAIEmbeddings(
    model=os.getenv("embedding_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url"),
    check_embedding_ctx_length=False
)

vector_stores = Chroma(
    collection_name="test",
    embedding_function=embedding_model,
    persist_directory="D:/Agent-Learning/code/2026-08-19/chromadb"
)

# # 读取文件
# csv_loader = CSVLoader(
#     file_path="D:/Agent-Learning/code/2026-08-19/data/info.csv",
#     source_column="source",
#     encoding="utf-8"
# )

# # 生成[Document,Document...]
# documents = csv_loader.load()
# # print(documents)

# # 内存向量存储器添加向量文件
# vector_stores.add_documents(
#     documents=documents,  # 已经是[Doucment]格式的文本文件
#     ids=["id"+str(i) for i in range(1,len(documents)+1)] # 对应的id编号
# )

# # 内存向量存储器删除向量文件
# vector_stores.delete(
#     ids=["id1","id2"]    # 删除指定id的向量文件
# )

# 计算内存向量存储器里的向量与query的相似度,返回[Document,Document...]
result = vector_stores.similarity_search(
    query="python是不是简单易学",
    k=3,
    filter={"source":"黑马程序员"}
)
print(result)

"""
1、没有加filter：
[Document(id='id5', metadata={'source': '传智教育', 'row': 4}, page_content='source: 传智教育\ninfo: Python学起来很简单的'), 
Document(id='id7', metadata={'row': 6, 'source': '黑马程序员'}, page_content='source: 黑马程序员\ninfo: 努力带来成就，Python助力辉煌'), 
Document(id='id4', metadata={'row': 3, 'source': '黑马程序员'}, page_content='source: 黑马程序员\ninfo: AI和Python是下一个十年的风口')]

2、加了filter："source":"黑马程序员"
[Document(id='id7', metadata={'row': 6, 'source': '黑马程序员'}, page_content='source: 黑马程序员\ninfo: 努力带来成就，Python助力辉煌'), 
Document(id='id4', metadata={'source': '黑马程序员', 'row': 3}, page_content='source: 黑马程序员\ninfo: AI和Python是下一个十年的风口'), 
Document(id='id6', metadata={'source': '黑马程序员', 'row': 5}, page_content='source: 黑马程序员\ninfo: 学习Python键盘敲烂月薪过万')]
"""