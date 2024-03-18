import logging
from datetime import datetime

from dash import html, dcc
import dash_daq as daq
import numpy as np

from .base_dashboard_component import BaseDashboardComponent


logger = logging.getLogger(__name__)


class StatsPanelComponent(BaseDashboardComponent):
    def build(self):
        return self.build_quick_stats_panel()

    def build_quick_stats_panel(self):
        last_update_datetime = self.messages_df['scraped_at_timestamp'].values[-1]
        last_update_datetime = np.datetime_as_string(last_update_datetime, unit='s')
        last_update_datetime = datetime.strptime(last_update_datetime, '%Y-%m-%dT%H:%M:%S')
        last_update_datetime = last_update_datetime.strftime('%Y-%m-%d %H:%M:%S')

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
                            value=f"{len(self.messages_df)}",
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
                                html.Span(f"{last_update_datetime}", style={"backgroundColor": "#1e2130"}),
                            ],
                            style={"font-size": "1.2em", "color": "#92e0d3", "margin": "20px"}
                        )
                    ],
                ),
                html.Div(
                    id="utility-card",
                    children=[
                        dcc.Loading(
                            id="loading-channel",
                            type="circle",  # or "default"
                            children=[
                                html.Button('Run scraping', id='run-scraping-channel', value=f"{self.channel_id}",
                                            n_clicks=0),
                                html.Div(id="loading-channel-scraping-output")],
                        ),

                    ],
                ),
            ],
        )
