from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableWithMessageHistory
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history


def print_prompt(prompt):
    print("-" * 50)
    print(prompt.to_string())
    print("-" * 50)
    return prompt   

class RagServer(object):
    def __init__(self):

        self.vetor_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考材料为主，简洁和专业地回答用户的问题，参考材料：{context}。"),
                ("system", "并且提供用户的对话历史记录，如下："),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "用户提问：{input}"),
            ]
        )

        self.chat_model = ChatTongyi(model=config.chat_model_name)

        self.chain = self.get_chain()

    def get_chain(self):
        """构建RAG的链式调用"""
        retriever = self.vetor_service.get_retriever()

        def format_document(docs:list[Document]):
            if not docs:
                return "没有相关信息"
            
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据:{doc.metadata}\n\n"

            return formatted_str   
     
        def temp1(value):
            return value["input"]
        
        def temp2(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["chat_history"] = value["input"]["chat_history"]
            return new_value


        chain = (
            {
                "input": RunnablePassthrough(), 
                "context": RunnableLambda(temp1) | retriever | format_document
            } | RunnableLambda(temp2) |self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="chat_history"

        )

        return conversation_chain
    
if __name__ == "__main__":
    session_config = {
        "configurable": {"session_id": "user_001"}
    }

    res = RagServer().chain.invoke({"input": "晚饭想吃点清淡的，学校食堂有什么推荐的吗？"}, session_config)
    print(res)