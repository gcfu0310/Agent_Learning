import config_data as config
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os
load_dotenv()

class VectorStoreService():
    def __init__(self,embedding):
        self.embedding = embedding
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )

    def get_retriever(self):
        """返回向量检索器，方便后续入链"""
        return self.chroma.as_retriever(search_kwargs={"k":config.similarity_threshold})

if __name__ == "__main__":
    embedding_model = OpenAIEmbeddings(
        model=os.getenv("embedding_model"),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv("base_url"),
        check_embedding_ctx_length=False
    )
    vectstoreservice = VectorStoreService(embedding=embedding_model)
    retriever = vectstoreservice.get_retriever()

    content = "我体重200斤，推荐适合我的衣服尺码"
    print(retriever.invoke(input=content))