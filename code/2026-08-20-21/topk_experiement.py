import os
import config_data_1 as config
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
    file = "D:/Agent-Learning/code/2026-08-20-21/data/洗涤养护.txt"
    with open(file,'r',encoding="utf-8") as f:
        content = f.read()

    service = KnowledgeBaseService()
    print(service.upload_by_str(content,"textfiles"))

    query = "秋季羊毛或羊绒衣物应该如何清洗、晾干和收纳，才能避免缩水、变形和虫蛀？"

    results = service.chroma.similarity_search_with_score(
        query=query,
        k=3
    )

    for result in results:
        print(result)


"""
1、chunk_size=200,chunk_overlap=40,top-k结果
[跳过]内容已经存在知识库中
(Document(id='68a2a88c-3c00-45db-bd9a-d267c3fa00e8', metadata={'source': 'textfiles', 'operator': 'Mr.Fu', 'create_time': '2026-08-21 13:40:06'}, page_content='三、秋季服装（羊毛 、羊绒、厚牛仔、灯芯绒、麂皮绒）\n\n1. 羊毛/羊绒材质（秋季羊毛衫、薄羊绒大衣）\n\n洗涤：优先干洗；手洗用羊毛专用洗涤剂，水温≤20℃，浸泡≤15分钟，轻轻按压；禁止机洗、搓揉、拧绞。\n\n养护：平铺阴干，避免悬挂拉伸；收纳时放防虫蛀剂（樟脑丸、薰衣草香包），透气布袋包裹；宽肩悬挂或折叠收纳，避免重压。\n\n2. 厚牛仔材质（秋季牛仔外套、厚牛仔裤）'), 0.38488245010375977)
(Document(id='69e8f297-60c1-4094-8adf-5f62d5688b3a', metadata={'source': 'textfiles', 'operator': 'Mr.Fu', 'create_time': '2026-08-21 13:40:06'}, page_content='养护：阴凉阴干，避 免暴晒和高温烘烤；收纳折叠平放，避免尖锐物体勾划；穿着时避免粗糙物体摩擦。\n\n4. 雪纺材质（夏季连衣裙、防晒衫）\n\n洗涤：手洗优先，水温≤30℃，中性洗涤剂轻轻漂洗；机洗用洗衣袋，选轻柔模式；禁止用力拧绞。\n\n养护：阴凉阴干，悬挂时用细衣架避免勾丝；收纳折叠时垫一层薄纸，防止粘连；轻微褶皱用低温蒸汽熨烫。\n\n三、秋季服装（羊毛、羊绒、厚牛仔、灯芯绒、麂皮绒）'), 0.4998341202735901)
(Document(id='3d74efa2-ee0a-482f-8e41-eb4968dbae14', metadata={'operator': 'Mr.Fu', 'create_time': '2026-08-21 13:40:06', 'source': 'textfiles'}, page_content='养护：阴凉阴干，晾 晒时反面朝上；收纳时折叠，避免重压破坏绒面；熨烫用低温蒸汽，熨斗垫薄布，顺绒方向熨烫。\n\n4. 麂皮绒材质（秋季麂皮绒外套、夹克）\n\n洗涤：建议干洗；人造麂皮可手洗，水温≤30℃，中性洗涤剂轻轻按压；禁止机洗、漂白、用力拧绞。\n\n养护：阴凉阴干，避免暴晒和高温；收纳时悬挂，避免折叠产生折痕；表面灰尘用软毛刷轻轻刷除。\n\n四、冬季服装（羽绒服、厚羊毛大衣、加绒牛仔 、保暖内衣）'), 0.5927975177764893)
2、chunk_size=150,chunk_overlap=0,top-k结果：
(Agent) PS D:\Agent-Learning\code\2026-08-20-21> python .\topk_experiement.py
[成功]成功创建内容
(Document(id='6d33c812-ea90-4064-a28a-8b4b596fa52d', metadata={'source': 'textfiles', 'create_time': '2026-08-21 13:50:39', 'operator': 'Mr.Fu'}, page_content='养护：阴凉阴干，悬 挂时用细衣架避免勾丝；收纳折叠时垫一层薄纸，防止粘连；轻微褶皱用低温蒸汽熨烫。\n\n三、秋季服装（羊毛、羊绒、厚牛仔、灯芯绒、麂皮绒）\n\n1. 羊毛/羊绒材质（秋季羊毛衫、薄羊绒大衣）'), 0.379678338766098)
(Document(id='bcafc43b-a630-4820-8d80-2840bbe879ef', metadata={'create_time': '2026-08-21 13:50:39', 'operator': 'Mr.Fu', 'source': 'textfiles'}, page_content='洗涤：优先干洗；手 洗用羊毛专用洗涤剂，水温≤20℃，浸泡≤15分钟，轻轻按压；禁止机洗、搓揉、拧绞。\n\n养护：平铺阴干，避免悬挂拉伸；收纳时放防虫蛀剂（樟脑丸、薰衣草香包），透气布袋包裹；宽肩悬挂或折叠收纳，避免重压。\n\n2. 厚牛仔材质（秋季牛仔外套、厚牛仔裤）'), 0.49165818095207214)
(Document(id='5fd0a956-f9f3-4240-ab1f-0b64fd6003d9', metadata={'create_time': '2026-08-21 13:50:39', 'operator': 'Mr.Fu', 'source': 'textfiles'}, page_content='洗涤：必须干洗，干 洗能保护羊毛纤维弹性和柔软度；禁止水洗、机洗，避免纤维毡化、缩水。\n\n养护：悬挂收纳用宽肩无痕衣架，远离潮湿和高温；收纳前拍打去除灰尘，放防虫蛀剂；避免尖锐物体勾划。\n\n3. 加绒牛仔材质（冬季加绒牛仔裤、加绒牛仔外套）'), 0.5333986878395081)
[备注]：当chunk_size=100,overlap=0时，出现以下报错：
(Agent) PS D:\Agent-Learning\code\2026-08-20-21> python .\topk_experiement.py
Traceback (most recent call last):
  File "D:\Agent-Learning\code\2026-08-20-21\topk_experiement.py", line 97, in <module>
    print(service.upload_by_str(content,"textfiles"))
          ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "D:\Agent-Learning\code\2026-08-20-21\topk_experiement.py", line 81, in upload_by_str
    self.chroma.add_texts( # 内容添加进向量库
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
        texts=knowledge_chunks,
        ^^^^^^^^^^^^^^^^^^^^^^^
        metadatas=[metadata for _ in range(len(knowledge_chunks))]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "D:\Agent-Learning\.venv\Lib\site-packages\langchain_chroma\vectorstores.py", line 627, in add_texts
    embeddings = self._embedding_function.embed_documents(texts)
  File "D:\Agent-Learning\.venv\Lib\site-packages\langchain_openai\embeddings\base.py", line 744, in embed_documents
    response = self.client.create(
        input=texts[i : i + chunk_size_], **client_kwargs
    )
  File "D:\Agent-Learning\.venv\Lib\site-packages\openai\resources\embeddings.py", line 136, in create
    return self._post(
           ~~~~~~~~~~^
        "/embeddings",
        ^^^^^^^^^^^^^^
    ...<9 lines>...
        cast_to=CreateEmbeddingResponse,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "D:\Agent-Learning\.venv\Lib\site-packages\openai\_base_client.py", line 1375, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
                           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Agent-Learning\.venv\Lib\site-packages\openai\_base_client.py", line 1148, in request
    raise self._make_status_error_from_response(err.response) from None
openai.BadRequestError: Error code: 400 - {'error': {'message': '<400> InternalError.Algo.InvalidParameter: Value error, batch size is invalid, it should not be larger than 20.: input.contents', 'type': 'InvalidParameter', 'param': None, 'code': 'InvalidParameter'}, 'id': '2ad01819-76b0-9e35-a8f2-f59eed381df7', 'request_id': '2ad01819-76b0-9e35-a8f2-f59eed381df7'}
故增加chunk_size值到150
"""

