from abc import ABC, abstractmethod


class BaseDatabaseHandler(ABC):
    @abstractmethod
    def store_message(self, chat_id, message_id, content):
        pass

    @abstractmethod
    def store_comment(self, chat_id, message_id, comment_id, content):
        pass

    @abstractmethod
    def get_messages_by_chat_id(self, chat_id):
        pass

    @abstractmethod
    def get_comments_by_message_id(self, message_id):
        pass

    @abstractmethod
    def get_comments_by_chat_id(self, chat_id):
        pass
