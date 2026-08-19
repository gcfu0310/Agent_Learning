from dotenv import load_dotenv
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_loader = TextLoader(
    file_path="D:/Agent-Learning/code/2026-08-19/data/Python基础语法.txt",
    encoding="utf-8"
)

documents = text_loader.load()        # [Document]
# print(documents)                    # 把整个document输出出来
# print(len(documents))               # 列表里面就只有一个Document

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,                 # 分段的最大字符数
    chunk_overlap = 50,               # 分段之间允许重复的字符数
    # 文本自然段分隔的标记符
    separators=['\n\n','\n','','.','!','?',' ','。','！','？'],
    length_function = len             # 计算字符数的函数
)

split_docs = splitter.split_documents(documents)
print("分割为：",len(split_docs),"块")
print(split_docs[2])
