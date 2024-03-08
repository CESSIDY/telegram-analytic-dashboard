import logging

from dash import html, dcc, callback, Input, Output

from database import BaseDatabaseHandler
from loaders.channels import BaseChannelsLoader
from .base_component import BaseComponent
from web_app.components.channel_tab_components import ChannelTabDashboardManager


class ChannelTabsComponent(BaseComponent):
    def __init__(self, db_handler: BaseDatabaseHandler, channels_loader: BaseChannelsLoader,
                 channel_tab_dashboard_manager: ChannelTabDashboardManager):
        self.db_handler = db_handler
        self.channels_loader = channels_loader
        self.channels = self.db_handler.get_all_channels()
        self.channel_tab_dashboard_manager = channel_tab_dashboard_manager
        self.set_callbacks()

    def build(self):
        return self.build_channels_tabs()

    def set_callbacks(self):
        logging.info("ChannelTabsComponent: set_callbacks")
        callback(
            Output("app-content", "children"),
            Input("channels-tabs", "value"),
        )(self.build_tab_content)

    def build_tab_content(self, tab_switch: str):
        logging.info("ChannelTabsComponent: build_tab_content")
        channel_id = int(tab_switch.split('tab-')[-1])
        return [html.Div(
            id="status-container",
            children=self.channel_tab_dashboard_manager.set_channel(channel_id).build_components(),
        )]

    def build_channels_tabs(self):
        logging.info("ChannelTabsComponent: build_channels_tabs")
        channels_tabs = []

        if not self.channels:
            return self.render_non_channels_scraped_message()

        for channel in self.channels:
            tab = dcc.Tab(
                id=f"tab-{channel.chat_id}",
                label=channel.name,
                value=f"tab-{channel.chat_id}",
                className="custom-tab",
                selected_className="custom-tab--selected",
            )
            channels_tabs.append(tab)

        return html.Div(
            id="tabs",
            className="tabs",
            children=[
                dcc.Tabs(
                    id="channels-tabs",
                    value=f"tab-{self.channels[0].chat_id}" if self.channels else "",
                    className="custom-tabs",
                    children=channels_tabs,
                )
            ],
        )

    def render_non_channels_scraped_message(self):
        channels_count = len(self.channels_loader.get_all())
        return html.Div(
            id="non-channels",
            children=[
                html.P(
                    f"No channels was scraped click on button above to run scraping for ({channels_count}) channels")],
            style={"marginBottom": "20px", "textAlign": "center", "maxWidth": "600px"}
        )