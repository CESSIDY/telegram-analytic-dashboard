import logging

from dash import html, dcc, callback, Input, Output

from scraper import Scraper
from .base_component import BaseComponent
from web_app.components.page_components import ChannelTabsComponent


logger = logging.getLogger(__name__)


class ScrapersActionsComponent(BaseComponent):
    def __init__(self, channels_tabs_component: ChannelTabsComponent, scraper: Scraper):
        self.channels_tabs_component = channels_tabs_component
        self.scraper = scraper
        self.set_callbacks()

    def build(self):
        pass

    def set_callbacks(self):
        callback(
            [Output("app-content", "children", allow_duplicate=True),
             Output("loading-channel-scraping-output", "children")],
            [Input("run-scraping-channel", "value"),
             Input("run-scraping-channel", "n_clicks")],
            background=True,
            running=[
                (
                    Output("loading-channel-scraping-output", "style"),
                    {"visibility": "visible"},
                    {"visibility": "hidden"},
                ),
            ],
            prevent_initial_call=True
        )(self.run_channel_scraping)

        callback(
            [Output("app-container", "children"), Output("loading-channels-scraping-output", "children")],
            Input("run-scraping-channels", "n_clicks"),
            background=True,
            running=[
                (
                    Output("loading-channels-scraping-output", "style"),
                    {"visibility": "visible"},
                    {"visibility": "hidden"},
                ),
            ],
            prevent_initial_call=True
        )(self.run_channels_scraping)

    def run_channel_scraping(self, channel_id, n_clicks):
        if not n_clicks or n_clicks <= 0:
            return self.channels_tabs_component.build_tab_content(f"tab-{channel_id}"), None
        logger.info(f"Click on run scraping for channel {channel_id}")
        self.scraper.run_scraper(int(channel_id))
        logger.info(f"Completed scraping")
        return self.channels_tabs_component.build_tab_content(f"tab-{channel_id}"), None

    def run_channels_scraping(self, n_clicks):
        if not n_clicks or n_clicks <= 0:
            return [self.channels_tabs_component.build(), html.Div(id="app-content")], None
        logger.info(f"Click on run scraping for all channels {n_clicks}")
        self.scraper.run_scraper()
        logger.info(f"Completed scraping")
        return [self.channels_tabs_component.build(), html.Div(id="app-content")], None
