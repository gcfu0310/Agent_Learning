from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
import os

load_dotenv()
embeddings = OpenAIEmbeddings(
    model=os.getenv("embedding_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url"),
    check_embedding_ctx_length=False
)
query = embeddings.embed_query("Hello!I'm Sumimi")
docs = embeddings.embed_documents(["Hello!I'm Sumimi","Hello,I'm cute"])
print(f"query:{query}")
print(f"docs:{docs}")

o_embedding = OllamaEmbeddings(
    model="qwen3-embedding:4b"
)
query = o_embedding.embed_query("Hello!I'm Sumimi")
docs = o_embedding.embed_documents(["Hello!I'm Sumimi","Hello,I'm cute"])
print(f"query:{query}")
print(f"docs:{docs}")