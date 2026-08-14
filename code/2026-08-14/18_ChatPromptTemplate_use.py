from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

# messages的统一写法[{},{}]：列表里面套字典
# from_template()只能接入一条消息，from_messages()可以接入一个列表的消息
chatprompt_template = ChatPromptTemplate.from_messages(
    [
    ("system","你叫顶真珍珠，是一名藏族学生"),
    MessagesPlaceholder("history"), # MessagesPlaceholder作为占位符，让历史消息可以从外部导入，方便历史消息更新迭代
    ("human","雪豹怎么叫")
    ]
)

history = [
    ("human","牦牛怎么叫"),
    ("ai","哞~"),
    ("human","绵羊怎么叫"),
    ("ai","咩~")
]
chat_prompt_text = chatprompt_template.invoke(input={"history":history})
llm = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)
res = llm.invoke(input=chat_prompt_text)
print(res.content)