import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

def check_md5(md5_str:str):
    """检查传入的md5字符串是否已经被处理过了
    return True (已经被处理过),False(未被处理过)
    """
    if not os.path.exists(config.md5_path):
        # 文件不存在肯定未处理过
        open(config.md5_path,"w",encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path,"r",encoding="utf-8").readlines():
            line = line.strip() # 去除每行的开头和结尾的空格与换行
            if line == md5_str:
                return True # 代表已经处理过
        return False

def save_md5(md5_str:str):
    """将md5字符串加入md5文件"""
    with open(config.md5_path,"a",encoding="utf-8") as f: # 模式选择'a'代表追加，'w'会覆盖文件之前的内容
        f.write(md5_str+'\n')

def get_string_md5(input_str:str,encoding="utf-8"):
    """将字符串转换为md5格式的字符串"""

    # 将字符串转换为字节形式(二进制)
    str_bytes = input_str.encode(encoding=encoding)

    # 创建md5对象
    md5_obj = hashlib.md5() # 得到md5对象
    md5_obj.update(str_bytes) # 更新内容
    md5_hex = md5_obj.hexdigest() # 获得md5的十六进制字符串

    return md5_hex

class KnowledgeBaseService():
    def __init__(self):
        embedding_model = OpenAIEmbeddings(
            model=os.getenv("embedding_model"),
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url=os.getenv("base_url"),
            check_embedding_ctx_length=False
        )
        self.chroma = Chroma(
            collection_name=config.collection_name, # 数据库的表名
            embedding_function=embedding_model, # 向量模型
            persist_directory=config.persist_directory # 文件所在地址
        ) # 向量库对象
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, # 分割后的文本段最大长度
            chunk_overlap=config.chunk_overlap, # 连续文本段之间的字符重叠数量
            separators=config.separators, # 自然段落的划分符号
            length_function=len # 计算长度的函数
        ) # 分割器对象

    def upload_by_str(self,data:str,filename):
        """将传入的字符串向量化，存入向量数据库中"""
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"

        if len(data) > config.max_split_char_nums:
            knowledge_chunks = self.splitter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source":filename,
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"Mr.Fu"
        }
        self.chroma.add_texts( # 内容添加进向量库
            texts=knowledge_chunks,
            metadatas=[metadata for _ in range(len(knowledge_chunks))]
        )
        save_md5(md5_hex)
        return "[成功]成功创建内容"




if __name__ == "__main__":
    str1 = "sumimi"
    str2 = "sumimi"
    str3 = "Sumimi"

    # md5_1 = get_string_md5(str1)
    # md5_2 = get_string_md5(str2)
    # md5_3 = get_string_md5(str3) # 不管文本有多长，转成md5格式的长度都是一样的

    # # print(md5_1)
    # # print(md5_2)
    # # print(md5_3)
    
    # save_md5(md5_1)
    # print(check_md5(md5_2))
    service = KnowledgeBaseService()
    # print(service.upload_by_str(str1,"textfiles"))
    print(service.upload_by_str(str2,"textfiles"))

