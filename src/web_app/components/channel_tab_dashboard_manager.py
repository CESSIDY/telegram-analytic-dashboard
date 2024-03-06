from typing import List

from services import DBDataToPandasLoader
from . import BaseComponent


class ChannelTabDashboardManager:
    def __init__(self, db_handler):
        self.db_data_to_pandas_loader = DBDataToPandasLoader(db_handler)

        self.components: List[BaseComponent] = []
        self.messages_df = None

    def set_messages_df(self, channel_id):
        self.messages_df = self.db_data_to_pandas_loader.get_messages_df_by_channel_id(channel_id)
        [component.set_messages_df(self.messages_df) for component in self.components]
        return self

    def add_components(self, components: List[BaseComponent]):
        for component in components:
            self.add_component(component)
        return self

    def add_component(self, component: BaseComponent):
        self.components.append(component)
        return self

    def build_components(self):
        return [component.build() for component in self.components]

