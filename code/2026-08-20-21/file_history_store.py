from langchain_core.chat_history import BaseChatMessageHistory
from typing import Sequence
import os,json
from langchain_core.messages import BaseMessage,message_to_dict,messages_from_dict
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
load_dotenv()

def get_history(session_id):
    return FileChatMessageHistory(session_id)

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path="./chat_history"):
        self.session_id = session_id    # 存储会话id
        self.storage_path = storage_path    # 文件存放的文件夹地址

        self.file_path = os.path.join(self.storage_path,self.session_id)
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True) # 文件夹不存在，则创建文件夹

    def add_messages(self,messages:Sequence[BaseMessage]) -> None:
        # Sequence序列类似list、tuple
        all_messages = list(self.messages) # self.messages已有的会话记录
        all_messages.extend(messages)  # all_messages:[BaseMessage,BaseMessage,BaseMessage]

        # 为了存储到文件当中(直接存储BaseMessage，在文件当中是二进制的形式)，需要把原列表里面的内容转换成dict
        new_messages = [message_to_dict(message) for message in all_messages] # message_to_dit将单个BasaMessage实例转换成单个dict BaseMessage->dict
        # 将数据写入文件
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(new_messages,f)

    @property
    def messages(self)->list[BaseMessage]:
        # 当前文件内：list[{},{}...]
        try:
            with open(self.file_path,'r',encoding="utf-8") as f:
                messages_data = json.load(f)
            return messages_from_dict(messages_data) # message_from_dict将dicts序列转换成BaseMessage序列 [{},{}...] -> [BaseMessage,BaseMessage...]
        except FileNotFoundError:
            return []

    def clear(self)->None:
        with open(self.file_path,'w',encoding="utf-8") as f:
            json.dump([],f)