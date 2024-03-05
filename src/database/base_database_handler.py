from abc import ABC, abstractmethod
from typing import List

from .models import Channel, Message, Comment


class BaseDatabaseHandler(ABC):

    @abstractmethod
    def store_channel(self, chat_id, chat_name, content):
        pass

    @abstractmethod
    def store_message(self, chat_id, message_id, content):
        pass

    @abstractmethod
    def store_comment(self, chat_id, message_id, comment_id, content):
        pass

    @abstractmethod
    def get_all_channels(self) -> List[Channel]:
        pass

    @abstractmethod
    def get_messages_by_chat_id(self, chat_id) -> List[Message]:
        pass

    @abstractmethod
    def get_comments_by_message_id(self, message_id) -> List[Comment]:
        pass

    @abstractmethod
    def get_comments_by_chat_id(self, chat_id) -> List[Comment]:
        pass
