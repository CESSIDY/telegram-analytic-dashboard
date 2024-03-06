from abc import ABC, abstractmethod

from pandas import DataFrame


class BaseDashboardComponent(ABC):
    def __init__(self):
        self.messages_df: DataFrame | None = None
        self.channels_df: DataFrame | None = None
        self.channel_id: DataFrame | None = None

    def set_messages_df(self, messages_df: DataFrame):
        self.messages_df = messages_df.copy()
        return self

    def set_channels_df(self, channels_df: DataFrame):
        self.channels_df = channels_df.copy()
        return self

    def set_channel_id(self, channel_id):
        self.channel_id = channel_id
        return self

    @abstractmethod
    def build(self):
        pass
