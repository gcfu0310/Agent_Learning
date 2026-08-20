from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict,messages_from_dict,BaseMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
import os,json
load_dotenv()

Prompt = ChatPromptTemplate.from_messages(
    [
    ("system","你需要根据会话历史简单回答用户问题。会话历史："),
    MessagesPlaceholder("chat_history"),
    ("user","请回答用户提问:{user_input}")
    ]
)

def print_Prompt(prompt):
    print("="*20,prompt.to_string(),"="*20)
    return prompt

model = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)

base_chain = Prompt|print_Prompt|model|StrOutputParser()

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path="D:/Agent-Learning/code/2026-08-20/chat_history"):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path,self.session_id)
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_messages(self,message:BaseMessage):
        all_messages = list(self.messages)
        all_messages.extend(message)

        new_messages = [message_to_dict(message) for message in all_messages]

        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(new_messages,f)

    @property
    def messages(self):
        try:
            with open(self.file_path,'r',encoding="utf-8") as f:
                messages_data = json.load(f)
            return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self):
        with open(self.file_path,'w',encoding="utf-8") as f:
            json.dump([],f)

def get_history(session_id):
    return FileChatMessageHistory(session_id)

conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="user_input",
    history_messages_key="chat_history"
)

if __name__ == "__main__":
    session_config_1 = {
        "configurable":{
            "session_id":"user-001"
        }
    }
    session_config_2 = {
        "configurable":{
            "session_id":"user-001"
        }
    }

    res = conversation_chain.invoke(input={"user_input":"我最喜欢Python这款编程语言"},config=session_config_1)
    print("第一用户的第一次回答:",res)
    res = conversation_chain.invoke(input={"user_input":"我最喜欢TypeScript这款编程语言"},config=session_config_2)
    print("第二用户的第一次回答:",res)
    res = conversation_chain.invoke(input={"user_input":"我最喜欢哪款编程语言"},config=session_config_1)
    print("第一用户的第二次回答:",res)
    res = conversation_chain.invoke(input={"user_input":"我最喜欢哪款编程语言"},config=session_config_2)
    print("第二用户的第二次回答:",res)

"""
1、验证不同session_id时不互相干扰：
==================== System: 你需要根据会话历史简单回答用户问题。会话历史：
Human: 请回答用户提问:我最喜欢Python这款编程语言 ====================
第一用户的第一次回答: Python确实是一门非常强大且受欢迎的编程语言！它语法简洁、生态丰富，应用也非常广泛。

你平时最喜欢用它来做什么呢？是数据分析、Web开发、自动化脚本还是人工智能？
==================== System: 你需要根据会话历史简单回答用户问题。会话历史：
Human: 请回答用户提问:我最喜欢TypeScript这款编程语言 ====================
第二用户的第一次回答: TypeScript 确实是一门非常优秀的编程语言！它的静态类型检查和强大的工具链支持能大大提升代码的可维护性和开发体验。你最喜欢它的哪个特性呢？
==================== System: 你需要根据会话历史简单回答用户问题。会话历史：
Human: 我最喜欢Python这款编程语言
AI: Python确实是一门非常强大且受欢迎的编程语言！它语法简洁、生态丰富，应用也非常广泛。

你平时最喜欢用它来做什么呢？是数据分析、Web开发、自动化脚本还是人工智能？
Human: 请回答用户提问:我最喜欢哪款编程语言 ====================
第一用户的第二次回答: 您最喜欢的编程语言是Python。
==================== System: 你需要根据会话历史简单回答用户问题。会话历史：
Human: 我最喜欢TypeScript这款编程语言
AI: TypeScript 确实是一门非常优秀的编程语言！它的静态类型检查和强大的工具链支持能大大提升代码的可维护性和开发体验。你最喜欢它的哪个特性呢？
Human: 请回答用户提问:我最喜欢哪款编程语言 ====================
第二用户的第二次回答: 您最喜欢 TypeScript。
2、相同的session_id出现了会话记录污染的结果
==================== System: 你需要根据会话历史简单回答用户问题。会话历史：
Human: 请回答用户提问:我最喜欢Python这款编程语言 ====================
第一用户的第一次回答: Python确实是一门非常优秀的编程语言，语法简洁且应用广泛。请问有什么我可以帮您的吗？或者您想聊聊关于Python的什么话题呢？
==================== System: 你需要根据会话历史简单回答用户问题。会话历史：
Human: 我最喜欢Python这款编程语言
AI: Python确实是一门非常优秀的编程语言，语法简洁且应用广泛。请问有什么我可以帮您的吗？或者您想聊聊关于Python的什么话题呢？
Human: 请回答用户提问:我最喜欢TypeScript这款编程语言 ====================
第二用户的第一次回答: TypeScript确实是一门非常出色的编程语言，它的静态类型系统能让代码更健壮、更易于维护。请问有什么我可以帮您的吗？或者您想聊聊关于TypeScript的什么话题呢？
==================== System: 你需要根据会话历史简单回答用户问题。会话历史：
Human: 我最喜欢Python这款编程语言
AI: Python确实是一门非常优秀的编程语言，语法简洁且应用广泛。请问有什么我可以帮您的吗？或者您想聊聊关于Python的什么话题呢？
Human: 我最喜欢TypeScript这款编程语言
AI: TypeScript确实是一门非常出色的编程语言，它的静态类型系统能让代码更健壮、更易于维护。请问有什么我可以帮您的吗？或者您想聊聊关于TypeScript的什么话题呢？
Human: 请回答用户提问:我最喜欢哪款编程语言 ====================
第一用户的第二次回答: 根据我们的对话历史，您提到过最喜欢 **Python** 和 **TypeScript** 这两款编程语言。
==================== System: 你需要根据会话历史简单回答用户问题。会话历史：
Human: 我最喜欢Python这款编程语言
AI: Python确实是一门非常优秀的编程语言，语法简洁且应用广泛。请问有什么我可以帮您的吗？或者您想聊聊关于Python的什么话题呢？
Human: 我最喜欢TypeScript这款编程语言
AI: TypeScript确实是一门非常出色的编程语言，它的静态类型系统能让代码更健壮、更易于维护。请问有什么我可以帮您的吗？或者您想聊聊关于TypeScript的什么话题呢？
Human: 我最喜欢哪款编程语言
AI: 根据我们的对话历史，您提到过最喜欢 **Python** 和 **TypeScript** 这两款编程语言。
Human: 请回答用户提问:我最喜欢哪款编程语言 ====================
第二用户的第二次回答: 根据我们的对话历史，您提到过最喜欢 **Python** 和 **TypeScript**。
"""