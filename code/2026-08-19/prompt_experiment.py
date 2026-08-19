from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
load_dotenv()

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你是万事通，基于历史会话记录简短的回答用户的提问，会话记录："),
        MessagesPlaceholder("chat_history"),
        ("human","简短回答用户问题:{user_input}")
    ]
)

chat_history = [
    ("human","AI发展的那么快，我还需要手搓代码吗？"),
    ("ai","有必要手搓代码")
]

llm = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)

# str_parser = StrOutputParser()

chain = chat_prompt|llm
for chunk in chain.stream(input={"chat_history":chat_history,"user_input":"为什么还要手搓代码"}):
    if chunk.content:
        print(chunk.content,end="",flush=True)

"""
实验记录：
一、正常运行：
1. **懂原理**：掌握底层逻辑，避免被AI的“黑盒”误导。
2. **能排错**：AI生成的代码常有隐蔽Bug，需要人工调试与优化。
3. **做创新**：应对高度复杂的业务逻辑与从0到1的定制化需求。
4. **练思维**：保持编程直觉，提升架构设计与核心问题解决能力。
二、完全缺少user_input:
KeyError: "Input to ChatPromptTemplate is missing variables {'user_input'}.  
Expected: ['chat_history', 'user_input'] Received: ['chat_history']
三、变量名输入错误:
KeyError: "Input to ChatPromptTemplate is missing variables {'user_input'}.  Expected: ['chat_history', 'user_input'] 
Received: ['chat_history', 'input']
四、恢复正常运行:
1. **把控质量**：AI生成的代码可能有Bug或安全漏洞，需人工审查兜底。
2. **理解原理**：亲手写才能掌握底层逻辑，知其然更知其所以然。
3. **架构设计**：复杂的系统设计和特定业务逻辑仍需人来主导。
4. **锻炼思维**：手搓代码是培养编程思维和解决问题能力的必经之路。
"""