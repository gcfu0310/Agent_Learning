md5_path = "./md5.text"

# Chroma
collection_name = "rag"
persist_directory = "./chromadb"

# splitter
chunk_size = 1000
chunk_overlap = 100
separators = ['\n','\n\n','.','!','?','。','！','？']
max_split_char_nums = 1000

# retriever
similarity_threshold = 1

# RagService
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()

embedding_model = OpenAIEmbeddings(
    model=os.getenv("embedding_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url"),
    check_embedding_ctx_length=False
)

chat_model = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)

# session_id
session_config = {
    "configurable":{
        "session_id":"user-001"
    }
}