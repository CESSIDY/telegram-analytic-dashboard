import logging

from dash import html, dcc, callback, Input, Output
from dash.exceptions import PreventUpdate

from .telegram_component import TelegramComponent
from .base_component import BaseComponent
from web_app.components.page_components import ChannelTabsComponent
from web_app.components.page_components import TelegramAccountAuthComponent


logger = logging.getLogger(__name__)


class ScrapersActionsComponent(BaseComponent):
    def __init__(self, channels_tabs_component: ChannelTabsComponent,
                 telegram_account_auth_component: TelegramAccountAuthComponent):
        self.channels_tabs_component = channels_tabs_component
        self.telegram_account_auth_component = telegram_account_auth_component
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
            [Output("app-container", "children", allow_duplicate=True), Output("loading-channels-scraping-output", "children")],
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
            raise PreventUpdate  # self.channels_tabs_component.build_tab_content(f"tab-{channel_id}"), None
        if not self.telegram_account_auth_component.is_scraper_unlocked():
            raise PreventUpdate  # TODO Add some message about beasy with other process
        if not self.telegram_account_auth_component.is_authorized():
            return self.telegram_account_auth_component.build(), None

        logger.info(f"Click on run scraping for channel {channel_id}")
        self.telegram_account_auth_component.run_scraping(int(channel_id))
        logger.info(f"Completed scraping")

        return self.channels_tabs_component.build_tab_content(f"tab-{channel_id}"), None

    def run_channels_scraping(self, n_clicks):
        if not n_clicks or n_clicks <= 0:
            raise PreventUpdate  #[self.channels_tabs_component.build(), html.Div(id="app-content")], None
        if not self.telegram_account_auth_component.is_scraper_unlocked():
            raise PreventUpdate  # TODO Add some message about beasy with other process
        if not self.telegram_account_auth_component.is_authorized():
            return self.telegram_account_auth_component.build(), None

        logger.info(f"Click on run scraping for all channels {n_clicks}")
        self.telegram_account_auth_component.run_scraping()
        logger.info(f"Completed scraping")

        return [self.channels_tabs_component.build(), html.Div(id="app-content")], None
