from typing import List
import logging

import dash
from dash import dash_table, Input, Output, State, html, dcc, callback
import plotly.graph_objs as go
import dash_daq as daq
import dash_mantine_components as dmc
import pandas as pd

from database import BaseDatabaseHandler
from database.models import Channel, Message, Comment
from loaders.channels import BaseChannelsLoader
from scraper.base_scraper import BaseScraper
from utils import settings
from scraper import Scraper
from database import DatabaseHandler, DebugDatabaseHandler
from loaders.channels import JsonChannelsLoader
from loaders.accounts import JsonAccountsLoader

logger = logging.getLogger(__name__)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Telegram Channels Dashboard"
server = app.server
app.config["suppress_callback_exceptions"] = True

# https://github.com/bradley-erickson/dash-app-structure

db_handler = DatabaseHandler()
channels_loader = JsonChannelsLoader()
accounts_loader = JsonAccountsLoader()
scraper = Scraper(db_handler, channels_loader, accounts_loader)

channels_count = len(channels_loader.get_all())


def run_server():
    app.run_server(debug=settings.DASH_DEBUG, port=settings.DASH_PORT)


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Telegram Channels Dashboard"),
                ],
            ),
            html.Div(
                id="banner-scraping-button",
                children=[
                    html.Div(
                        children=[
                            html.H6(f"Click on button to run scraping for ({channels_count}) channels"),
                            html.Button(
                                id="run-scraping-channels", children="Run scraping", n_clicks=0
                            )
                        ],
                        style={"text-align": "center", 'display': 'flex'}
                    ),
                ],
            ),
        ],
    )


def build_channels_tabs():
    channels_tabs = []
    channels = db_handler.get_all_channels()

    if not channels:
        return render_non_channels_scraped_message()

    for channel in channels:
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
                value=f"tab-{channels[0].chat_id}" if channels else "",
                className="custom-tabs",
                children=channels_tabs,
            )
        ],
    )


def render_non_channels_scraped_message():
    channels_count = len(channels_loader.get_all())
    return html.Div(
        id="non-channels",
        children=[
            html.P(f"No channels was scraped click on button above to run scraping for ({channels_count}) channels")],
        style={"marginBottom": "20px", "textAlign": "center", "maxWidth": "600px"}
    )


def build_quick_stats_panel(channel_id, messages: List[Message]):
    messages_count = len(messages)
    last_update_timestamp = list(messages)[-1].timestamp
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-message-count",
                children=[
                    html.P("Messages count"),
                    daq.LEDDisplay(
                        id="messages-count",
                        value=f"{messages_count}",
                        color="#92e0d3",
                        backgroundColor="#1e2130",
                        size=40,
                    ),
                ],
            ),
            html.Div(
                id="card-last-update",
                children=[
                    html.P("Last update"),
                    html.Div(
                        children=[
                            html.Span(f"{last_update_timestamp}", style={"backgroundColor": "#1e2130"}),
                        ],
                        style={"font-size": "1.2em", "color": "#92e0d3", "margin": "20px"}
                    )
                ],
            ),
            html.Div(
                id="utility-card",
                children=[html.Button('Run scraping', id='run-scraping-channel', value=f"{channel_id}", n_clicks=0)],
            ),
        ],
    )


def build_top_panel():
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            # Metrics summary
            html.Div(
                id="metric-summary",
                className="eight columns",
                children=[
                    generate_section_banner("Metrics Summary"),
                    html.Div(
                        id="metric-div",
                        children=[],  # TODO Add some metrics
                    ),
                ],
            ),
            # Piechart
            html.Div(
                id="piechart-outer",
                className="four columns",
                children=[
                    generate_section_banner("% Some data"),
                    generate_piechart(),  # TODO Fill pie chart
                ],
            ),
        ],
    )


def generate_piechart():
    return dcc.Graph(
        id="piechart",
        figure={
            "data": [
                {
                    "labels": [],
                    "values": [],
                    "type": "pie",
                    "marker": {"line": {"color": "white", "width": 1}},
                    "hoverinfo": "label",
                    "textinfo": "label",
                }
            ],
            "layout": {
                "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True,
            },
        },
    )


def build_chart_panel():
    return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=[
            generate_section_banner("Some Chart"),
            dcc.Graph(
                id="some-chart",
                figure=go.Figure(
                    {
                        "data": [
                            {
                                "x": [],
                                "y": [],
                                "mode": "lines+markers",
                                "name": "some",
                            }
                        ],
                        "layout": {
                            "paper_bgcolor": "rgba(0,0,0,0)",
                            "plot_bgcolor": "rgba(0,0,0,0)",
                            "xaxis": dict(
                                showline=False, showgrid=False, zeroline=False
                            ),
                            "yaxis": dict(
                                showgrid=False, showline=False, zeroline=False
                            ),
                            "autosize": True,
                        },
                    }
                ),
            ),
        ],
    )


app.layout = html.Div(
        id="big-app-container",
        children=[
            build_banner(),
            html.Div(
                id="app-container",
                children=[
                    build_channels_tabs(),
                    # Main app
                    html.Div(id="app-content"),
                ],
            )
        ],
    )


@app.callback(
    Output("app-content", "children"),
    Input("channels-tabs", "value"),
)
def render_tab_content(tab_switch: str):
    channel_id = tab_switch.split('tab-')[-1]
    messages = db_handler.get_messages_by_chat_id(channel_id)
    return [html.Div(
        id="status-container",
        children=[
            build_quick_stats_panel(channel_id, messages),
            html.Div(
                id="graphs-container",
                children=[build_top_panel(), build_chart_panel()],
            ),
        ],
    )]


@app.callback(
    Output("app-content", "children", allow_duplicate=True),
    [Input("run-scraping-channel", "value"),
     Input("run-scraping-channel", "n_clicks")],
    prevent_initial_call=True
)
def run_channel_scraping(channel_id, n_clicks):
    if not n_clicks or n_clicks <= 0:
        return render_tab_content(f"tab-{channel_id}")
    logger.info(f"Click on run scraping for channel {channel_id}")
    scraper.run_scraper(int(channel_id))
    logger.info(f"Completed scraping")
    return render_tab_content(f"tab-{channel_id}")


@app.callback(
    Output("app-container", "children"),
    Input("run-scraping-channels", "n_clicks")
)
def run_channels_scraping(n_clicks):
    if not n_clicks or n_clicks <= 0:
        return [build_channels_tabs(), html.Div(id="app-content")]
    logger.info(f"Click on run scraping for all channels {n_clicks}")
    scraper.run_scraper()
    logger.info(f"Completed scraping")
    return [build_channels_tabs(), html.Div(id="app-content")]


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)
