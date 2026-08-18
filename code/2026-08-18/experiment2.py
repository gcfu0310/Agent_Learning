"""
验证："历史存储 ≠ 模型自动记忆"(基于InMemory)
实验结论：历史存储并不代表模型记忆
"""
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate,MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
load_dotenv()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你需要根据会话历史来简单回答用户的问题。会话历史："),
        MessagesPlaceholder("chat_history"),
        ("human","请回答以下问题：{input}")
    ]
)

llm = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)

str_parser = StrOutputParser()

def print_prompt(prompt):
    print("="*20,prompt.to_string(),"="*20)
    return prompt
# 定义一个基础chain
base_chain = prompt|print_prompt|llm|str_parser

# 对base_chain进行增强
store = {}
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 总结：取 session → 找 history → 注入 Prompt → 调模型 → 保存本轮 Human + AI → 下轮再注入。 
conversation_chain = RunnableWithMessageHistory(
    base_chain, # 被增强的原有chain
    get_history,# 通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="input",             # 表示用户输入在模板中的占位符
    history_messages_key="chat_history"     # 表示历史信息在模板中的占位符
)

if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id":"user_001"
        }
    }
    res = conversation_chain.invoke(input={"input":"小明家有两只边牧"},config=session_config)
    print("first try:",res)
    res = conversation_chain.invoke(input={"input":"小刚家有两只金毛"},config=session_config)
    print("second try:",res)

    # 删除之前的历史会话记录
    store.pop("user_001")

    res = conversation_chain.invoke(input={"input":"一共有几只狗"},config=session_config)
    print("third try:",res)

"""
实验输出：
==================== System: 你需要根据会话历史来简单回答用户的问题。会话历史：
Human: 请回答以下问题：小明家有两只边牧 ====================
first try: “小明家有两只边牧”是一个陈述句。请问您具体想问关于这两只边牧的什么问题呢？
==================== System: 你需要根据会话历史来简单回答用户的问题。会话历史：
Human: 小明家有两只边牧
AI: “小明家有两只边牧”是一个陈述句。请问您具体想问关于这两只边牧的什么问题呢？
Human: 请回答以下问题：小刚家有两只金毛 ====================
second try: “小刚家有两只金毛”是一个陈述句，不是问题哦。请问您具体想问关于小刚家金毛的什么问题呢？或者您是想比较小明家的边牧和小刚家的金毛吗？
==================== System: 你需要根据会话历史来简单回答用户的问题。会话历史：
Human: 请回答以下问题：一共有几只狗 ====================
third try: 抱歉，您没有提供任何会话历史或背景信息，所以我无法知道一共有几只狗。请提供相关的上下文！
"""