from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

chatprompt_template = ChatPromptTemplate.from_messages(
    [
    ("system","你叫顶真珍珠，是一名藏族学生"),
    MessagesPlaceholder("history"),
    ("human","雪豹怎么叫")
    ]
)

history = [
    ("human","牦牛怎么叫"),
    ("ai","哞~"),
    ("human","绵羊怎么叫"),
    ("ai","咩~")
]
llm = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)
chain = chatprompt_template | llm
# res = chain.invoke(input={"history":history})
# print(res.content)
for chunk in chain.stream(input={"history":history}):
    print(chunk.content,end="",flush=True)