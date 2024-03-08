from typing import List

from dash import html

from services import DBDataToPandasLoader
from .base_dashboard_component import BaseDashboardComponent
from .stats_panel_component import StatsPanelComponent


class ChannelTabDashboardManager:
    def __init__(self, db_handler):
        self.db_data_to_pandas_loader = DBDataToPandasLoader(db_handler)

        self.left_panel_component = StatsPanelComponent()
        self.components: List[BaseDashboardComponent] = []

    def set_channel(self, channel_id: int):
        self.set_channel_id(channel_id)
        self.set_messages_df(channel_id)
        return self

    def set_messages_df(self, channel_id):
        messages_df = self.db_data_to_pandas_loader.get_messages_df_by_channel_id(channel_id)
        [component.set_messages_df(messages_df) for component in self.components]
        self.left_panel_component.set_messages_df(messages_df)
        return self

    def set_channel_id(self, channel_id):
        [component.set_channel_id(channel_id) for component in self.components]
        self.left_panel_component.set_channel_id(channel_id)
        return self

    def add_components(self, components: List[BaseDashboardComponent]):
        for component in components:
            self.add_component(component)
        return self

    def add_component(self, component: BaseDashboardComponent):
        self.components.append(component)
        return self

    def build_components(self):
        return [
            self.left_panel_component.build(),
            html.Div(
                id="graphs-container",
                children=[component.build() for component in self.components],
            ),
        ]

