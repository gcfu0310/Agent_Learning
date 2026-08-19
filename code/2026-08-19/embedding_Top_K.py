from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
import numpy as np
load_dotenv()

embedding_model = OpenAIEmbeddings(
    model=os.getenv("embedding_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url"),
    check_embedding_ctx_length=False
)

documents = [
    "RAG 会先从知识库中检索与用户问题相关的文档，再把检索结果和问题一起交给大语言模型生成答案。它能够减少模型在专业知识问答中的幻觉。",

    "Embedding 模型可以把文本转换成向量。语义越接近的文本，其向量在空间中的距离通常越近，可以使用余弦相似度比较它们。",

    "文档切分会把较长的文件拆成多个文本块。chunk_size 太大可能引入无关信息，太小则可能丢失回答问题所需的上下文。",

    "Retriever 根据用户问题查找最相关的文本块，通常会返回相似度最高的 Top-k 文档，供后续 Prompt 和模型使用。",

    "Agent 可以根据任务选择并调用工具，然后观察工具返回的结果，再决定继续调用工具还是生成最终答案。",

    "成都位于中国西南地区，以熊猫、火锅和悠闲的生活方式闻名，也是一座重要的科技与文化城市。"
]

# query = "RAG 系统是怎样找到与用户问题最相关的知识片段的？"
query = "文本块切得太小会产生什么问题？"

# 单个文本计算向量，用embed_query
query_embed = embedding_model.embed_query(query)
# 多个文本计算向量，用embed_documents
documents_embed = embedding_model.embed_documents(documents)

# 相似度计算公式
def cosine_similarity(a,b):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

k = 2
temp = [] # 存储对应下标以及相似度 [[index,similarity]...]

# 计算每个文本和query之间的相似度并记录下标和相似度
for i,doc_embed in enumerate(documents_embed):
    s = cosine_similarity(query_embed,doc_embed)
    temp.append([i,s])

# 对相似度进行降序排序
temp = sorted(temp,key=lambda x:x[1],reverse=True)

# # 输出top_k原文以及相似度
for t in temp[:k]:
    print(f"原文：{documents[t[0]]},相似度：{t[1]}")

"""
实验1：使用query = "RAG 系统是怎样找到与用户问题最相关的知识片段的？"
实验记录1：
原文：RAG 会先从知识库中检索与用户问题相关的文档，再把检索结果和问题一起交给大语言模型生成答案。它能够减少模型在专业知识问答中的幻觉。,相似度：0.7619143795392098
原文：Retriever 根据用户问题查找最相关的文本块，通常会返回相似度最高的 Top-k 文档，供后续 Prompt 和模型使用。,相似度：0.6777447855024339

实验2：使用query = "文本块切得太小会产生什么问题？"
实验记录2：
原文：文档切分会把较长的文件拆成多个文本块。chunk_size 太大可能引入无关信息，太小则可能丢失回答问题所需的上下文。,相似度：0.663543349550224
原文：Retriever 根据用户问题查找最相关的文本块，通常会返回相似度最高的 Top-k 文档，供后续 Prompt 和模型使用。,相似度：0.3625651875021043

实验结论：
实验1的预期最高相似度是第5条，实际确实第一条
实验2符合预期
"""



