from dash import dash_table, html, dcc
import plotly.graph_objs as go
import dash_daq as daq
from pandas import DataFrame

from web_app.components.utils.basic_components import generate_section_banner
from .base_dashboard_component import BaseDashboardComponent


class MessageEngagementChartsComponent(BaseDashboardComponent):
    MOST_RECENT_MESSAGE_OFFSET = 3

    def set_messages_df(self, messages_df: DataFrame):
        super().set_messages_df(messages_df)
        self.messages_df = self.messages_df[:-self.MOST_RECENT_MESSAGE_OFFSET]

    def build(self):
        return self.build_chart_panel()

    def build_chart_panel(self, included_columns=None, is_group_by_date=False):
        if not included_columns:
            included_columns = {'views': 'Views', 'forwards': 'Forwards', 'reactions': 'Reactions'}
        x = list(range(len(self.messages_df)))

        if is_group_by_date:
            messages_df = self.messages_df.groupby(['date'])[list(included_columns.keys())].mean().reset_index()
            x = messages_df['date']
        charts_data = []
        for k, v in included_columns.items():
            chart = {
                "x": x,
                "y": self.messages_df[k],
                "mode": "lines+markers",
                "name": v,
            }
            charts_data.append(chart)

        return html.Div(
            id="control-chart-container",
            className="twelve columns",
            children=[
                generate_section_banner("Message Engagement Trends Over Time"),
                dcc.Graph(
                    id="some-chart",
                    figure=go.Figure(
                        {
                            "data": charts_data,
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
