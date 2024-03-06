from abc import ABC, abstractmethod

from pandas import DataFrame


class BaseComponent(ABC):
    def __init__(self):
        self.messages_df = None

    def set_messages_df(self, messages_df: DataFrame):
        self.messages_df = messages_df.copy()
        return self

    @abstractmethod
    def build(self):
        pass
