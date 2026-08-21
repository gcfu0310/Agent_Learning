import config_data as config
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from vector_stores import VectorStoreService
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from file_history_store import get_history
from langchain_core.runnables import RunnableWithMessageHistory

class RagService():
    def __init__(self):
        self.retriever = VectorStoreService(config.embedding_model).get_retriever()
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的已知参考资料为主，"
                 "简洁和专业的回答用户问题。参考资料:\n{context}"),
                ("system", "并且我提供用户的对话历史记录，如下："),
                MessagesPlaceholder("history"),
                ("human","请回答用户提问：{input}")
            ]
        )
        self.chat_model = config.chat_model
        self.chain = self.__get_chain()

    def __get_chain(self):
        """执行整条链"""
        def format_func(documents:list[Document]):
            if not documents:
                return "无参考资料"
            text = ""
            for doc in documents:
                text += f"[文档片段]:{doc.page_content}\n[文档元数据]:{doc.metadata}\n\n"
            return text

        def print_prompt(prompt):
            print("="*20)
            print(prompt.to_string())
            print("="*20)
            return prompt

        def format_from_retriever(value:dict)->str:
            """提取传入字典的input值作为检索器的输入"""
            return value["input"]

        def format_from_prompt_template(value:dict):
            """提取列表中的input，context，history"""
            # {input, context, history}
            new_values = {}
            new_values["input"] = value["input"]["input"]
            new_values["history"] = value["input"]["history"]
            new_values["context"] = value["context"]
            return new_values
        
        chain = (
            {
                "input":RunnablePassthrough(),
                "context":RunnableLambda(format_from_retriever)|self.retriever|format_func
            }|RunnableLambda(format_from_prompt_template)|self.prompt_template|print_prompt|self.chat_model|StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            history_messages_key="history",
            input_messages_key="input"
        )
        return conversation_chain

if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id":"user-001"
        }
    }
    res = RagService().chain.invoke(input={"input":"冬天适合穿什么颜色的衣服？"},config=session_config)
    print(res)
    

    
