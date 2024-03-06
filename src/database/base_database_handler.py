from abc import ABC, abstractmethod
from typing import List

from .models import Channel, Message, Comment


class BaseDatabaseHandler(ABC):

    @abstractmethod
    def store_channel(self, channel_id, chat_name, content):
        pass

    @abstractmethod
    def store_message(self, channel_id, message_id, content):
        pass

    @abstractmethod
    def store_comment(self, channel_id, message_id, comment_id, content):
        pass

    @abstractmethod
    def get_all_channels(self) -> List[Channel]:
        pass

    @abstractmethod
    def get_messages_by_channel_id(self, channel_id) -> List[Message]:
        pass

    @abstractmethod
    def get_comments_by_message_id(self, message_id) -> List[Comment]:
        pass

    @abstractmethod
    def get_comments_by_channel_id(self, channel_id) -> List[Comment]:
        pass
