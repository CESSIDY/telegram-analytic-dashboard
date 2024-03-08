from dash import html, dcc

from database import BaseDatabaseHandler
from loaders.channels import BaseChannelsLoader
from .base_component import BaseComponent


class BannerComponent(BaseComponent):
    def __init__(self, channels_loader: BaseChannelsLoader):
        self.channels_loader = channels_loader
        self.channels = self.channels_loader.get_all()

    def build(self):
        return self.build_banner()

    def build_banner(self):
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
                                dcc.Loading(
                                    id="loading-channels",
                                    type="circle",  # or "default"
                                    children=[html.Button(
                                        id="run-scraping-channels",
                                        children=f"Run scraping for ({len(self.channels)}) channels", n_clicks=0
                                    ),
                                        html.Div(id="loading-channels-scraping-output")],
                                ),
                            ],
                            style={"text-align": "center", 'display': 'flex'}
                        ),
                    ],
                ),
            ],
        )
