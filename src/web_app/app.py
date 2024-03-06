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
from loaders.accounts import JsonAccountsLoader
from .components.page_components import (ChannelTabsComponent, BannerComponent)
from .components.channel_tab_components import (ChannelTabDashboardManager,
                                                MessageEngagementChartsComponent)

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
accounts_loader = JsonAccountsLoader()
scraper = Scraper(db_handler, channels_loader, accounts_loader)

channel_tab_dashboard_manager = ChannelTabDashboardManager(db_handler).add_components(
    [
        MessageEngagementChartsComponent(),
        MessageEngagementChartsComponent(),
        MessageEngagementChartsComponent(),
    ]
)

channels_tabs_component = ChannelTabsComponent(db_handler, channels_loader)
banner_component = BannerComponent(db_handler, channels_loader)

channels_count = len(channels_loader.get_all())


def run_server():
    app.run_server(debug=settings.DASH_DEBUG, port=settings.DASH_PORT)


app.layout = html.Div(
        id="big-app-container",
        children=[
            banner_component.build(),
            html.Div(
                id="app-container",
                children=[
                    channels_tabs_component.build(),
                    # Main app
                    html.Div(id="app-content"),
                ],
            )
        ],
    )


@app.callback(
    Output("app-content", "children"),
    Input("channels-tabs", "value"),
    background=True
)
def render_tab_content(tab_switch: str):
    channel_id = tab_switch.split('tab-')[-1]
    return [html.Div(
        id="status-container",
        children=channel_tab_dashboard_manager.set_channel(channel_id).build_components(),
    )]


@app.callback(
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
)
def run_channel_scraping(channel_id, n_clicks):
    if not n_clicks or n_clicks <= 0:
        return render_tab_content(f"tab-{channel_id}"), None
    logger.info(f"Click on run scraping for channel {channel_id}")
    scraper.run_scraper(int(channel_id))
    logger.info(f"Completed scraping")
    return render_tab_content(f"tab-{channel_id}"), None


@app.callback(
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
)
def run_channels_scraping(n_clicks):
    if not n_clicks or n_clicks <= 0:
        return [channels_tabs_component.build(), html.Div(id="app-content")], None
    logger.info(f"Click on run scraping for all channels {n_clicks}")
    scraper.run_scraper()
    logger.info(f"Completed scraping")
    return [channels_tabs_component.build(), html.Div(id="app-content")], None
