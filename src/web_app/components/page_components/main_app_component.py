import logging

from dash import html, dcc, callback, Input, Output, State

from scraper import Scraper
from .base_component import BaseComponent
from web_app.components.page_components import ChannelTabsComponent, BannerComponent

logger = logging.getLogger(__name__)


class MainAppComponent(BaseComponent):
    def __init__(self, banner_component: BannerComponent, channels_tabs_component: ChannelTabsComponent):
        self.banner_component = banner_component
        self.channels_tabs_component = channels_tabs_component

    def build(self):
        return self.build_main_app_page()

    def build_main_app_page(self):
        return html.Div(
            id="big-app-container",
            children=[
                self.banner_component.build(),
                html.Div(
                    id="app-container",
                    children=[
                        self.channels_tabs_component.build(),
                        # Main app
                        html.Div(id="app-content"),
                    ],
                )
            ],
        )
