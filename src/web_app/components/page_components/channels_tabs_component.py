from dash import html, dcc

from .base_component import BaseComponent


class ChannelTabsComponent(BaseComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channels = self.db_handler.get_all_channels()

    def build(self):
        return self.build_channels_tabs()

    def build_channels_tabs(self):
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