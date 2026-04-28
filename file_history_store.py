import os, json
from typing import Sequence, List  # 新增：导入类型注解所需模块
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_core.messages import message_to_dict, messages_from_dict,BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory



def get_history(session_id):
    return FileChatMessageHistory(session_id, storage_path="chat_histories")


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        super().__init__()
        self.session_id = session_id   #会话id
        self.storage_path = storage_path   #不同会话id的存储文件，所在文件的路径
        self.file_path = os.path.join(self.storage_path, self.session_id)

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_message(self, message):
        super().add_message(message)
        with open(self.file_path, "w") as f:
            json.dump([message_to_dict(m) for m in self.messages], f, ensure_ascii=False, indent=2)
    def add_messages(self, messages: Sequence[BaseMessage])-> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)
        
        new_messages = [message_to_dict(message) for message in all_messages]

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

    @property   #通过装饰器将messages方法变为成员属性
    def messages(self)->List[BaseMessage]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_dict = json.load(f)
                return messages_from_dict(messages_dict)
        
        except FileNotFoundError:
            return []
        
    def clear(self)-> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)