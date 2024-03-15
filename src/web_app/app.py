from typing import List
import logging
import time

import dash
from dash import dash_table, Input, Output, State, html, dcc, callback, CeleryManager
import plotly.graph_objs as go
import dash_daq as daq
import dash_mantine_components as dmc
import pandas as pd
from celery import Celery

from utils import settings
from scraper import Scraper
from database.handlers import DatabaseHandler
from loaders.channels import JsonChannelsLoader

from .components.page_components import (ChannelTabsComponent, BannerComponent, ScrapersActionsComponent,
                                         MainAppComponent, TelegramAccountAuthComponent)
from .components.channel_tab_components import (ChannelTabDashboardManager,
                                                MessageEngagementChartsComponent,
                                                MessageEmojisChartsComponent,
                                                MessageWordCloudChartsComponent)

logger = logging.getLogger(__name__)

celery_app = Celery(__name__, broker=settings.REDIS_URL, backend=settings.REDIS_URL)
background_callback_manager = CeleryManager(celery_app)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    background_callback_manager=background_callback_manager,
    title="Telegram Channels Dashboard"
)
server = app.server
app.config["suppress_callback_exceptions"] = True

# DBDataToPandasLoader
db_handler = DatabaseHandler()
channels_loader = JsonChannelsLoader()
scraper = Scraper(db_handler, channels_loader)

channel_tab_dashboard_manager = ChannelTabDashboardManager(db_handler).add_components(
    [
        MessageEngagementChartsComponent(),  # TODO: Maybe add component_name here
        MessageEmojisChartsComponent(),
        MessageWordCloudChartsComponent(),
    ]
)

channels_tabs_component = ChannelTabsComponent(db_handler=db_handler,
                                               channels_loader=channels_loader,
                                               channel_tab_dashboard_manager=channel_tab_dashboard_manager)

banner_component = BannerComponent(channels_loader)

main_app_component = MainAppComponent(banner_component, channels_tabs_component)

telegram_account_auth_component = TelegramAccountAuthComponent(scraper=scraper, main_app_component=main_app_component)

scrapers_actions_components = ScrapersActionsComponent(channels_tabs_component, telegram_account_auth_component)


def run_server():
    app.run_server(debug=settings.DASH_DEBUG, port=settings.DASH_PORT)


app.layout = html.Div(id='main-app-component', children=[main_app_component.build()])
