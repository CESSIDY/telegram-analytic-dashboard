from abc import ABC, abstractmethod

from pandas import DataFrame
from services import DBDataToPandasLoader


class BaseDashboardComponent(ABC):
    def __init__(self):
        self.messages_df: DataFrame | None = None
        self.channels_df: DataFrame | None = None
        self.channel_id: DataFrame | None = None
        self.db_data_to_pandas_loader: DBDataToPandasLoader = None
        self.set_callbacks()

    def set_messages_df(self, messages_df: DataFrame):
        self.messages_df = messages_df.copy()
        return self

    def set_channels_df(self, channels_df: DataFrame):
        self.channels_df = channels_df.copy()
        return self

    def set_db_data_to_pandas_loader(self, db_data_to_pandas_loader: DBDataToPandasLoader):
        self.db_data_to_pandas_loader = db_data_to_pandas_loader
        return self

    def set_channel_id(self, channel_id):
        self.channel_id = channel_id
        return self

    def set_callbacks(self):
        pass

    @abstractmethod
    def build(self):
        pass
