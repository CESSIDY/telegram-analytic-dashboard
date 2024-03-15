import logging

from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from pandas import DataFrame

from web_app.components.utils.basic_components import generate_section_banner
from .base_dashboard_component import BaseDashboardComponent

logger = logging.getLogger(__name__)


class MessageEngagementChartsComponent(BaseDashboardComponent):
    MOST_RECENT_MESSAGE_OFFSET = 3  # TODO: Remove just messages for N last days (give user to decide)
    DEFAULT_INCLUDED_COLUMNS = ['views', 'forwards', 'reactions']

    def set_messages_df(self, messages_df: DataFrame):
        super().set_messages_df(messages_df)
        self.messages_df = self.messages_df[:-self.MOST_RECENT_MESSAGE_OFFSET]

    def build(self):
        return html.Div(
            className='control-chart-container',
            children=[
                generate_section_banner('Message Engagement Trends Over Time'),
                self.build_interacted_components(),
                dcc.Graph(
                    id='message-engagement-linechart',
                    figure=go.Figure(self.build_chart_figure())
                )
            ],
        )

    def set_callbacks(self):
        callback(
            [Output('message-engagement-linechart', 'figure'),
             Output('loading-message-engagement-charts-output', 'children')],
            [Input('build-message-engagement-charts', 'n_clicks')],
            [State('chart-panel-columns-checklist', 'value'),
             State('chart-panel-group-by-date', 'value')],
            # background=True
        )(self.build_chart_figure_callback)

    def build_chart_figure_callback(self, n_click, included_columns, is_group_by_date):
        return self.build_chart_figure(n_click, included_columns, is_group_by_date), None

    def build_interacted_components(self):
        return html.Div(
            [
                html.P(
                    [
                        dcc.Loading(
                            id='loading-message-engagement-charts',
                            type='circle',  # or default
                            children=[
                                dbc.Button(
                                    id='build-message-engagement-charts',
                                    children='Build', n_clicks=0, outline=True
                                ),
                                html.Div(id='loading-message-engagement-charts-output')
                            ],
                        )
                    ],
                    style={'display': 'inline-block', 'margin-left': '20px', 'margin-right': '20px', 'vertical-align': 'middle'}
                ),
                html.Div([
                    html.Div(
                        [
                            html.P(
                                'Included columns:',
                                className='auto__p',
                                style={'display': 'inline-block', 'margin-right': '10px', 'margin-left': '10px'}
                            ),
                            dcc.Checklist(
                                self.DEFAULT_INCLUDED_COLUMNS,
                                self.DEFAULT_INCLUDED_COLUMNS,
                                id='chart-panel-columns-checklist',
                                inline=True,
                                style={'display': 'inline-block'}
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            dcc.Checklist(
                                id='chart-panel-group-by-date',
                                options=[
                                    {'label': 'Group by date', 'value': True}
                                ],
                                inline=True,
                                #switch=True, from dbc
                                value=[],
                                inputClassName='auto__checkbox',
                                labelClassName='auto__label',
                                style={'display': 'inline-block', 'margin-right': '10px', 'margin-left': '10px'}
                            ),
                        ],
                        className='auto__container',
                    )],
                    style={'display': 'inline-block', 'vertical-align': 'middle'}
                )
            ],
            className='auto__container',
        )

    def build_chart_figure(self, n_click=1, included_columns=None, is_group_by_date=False):
        if n_click <= 0:
            raise PreventUpdate
        if not included_columns:
            included_columns = self.DEFAULT_INCLUDED_COLUMNS

        if is_group_by_date:
            messages_df = self.messages_df.groupby(['date'])[included_columns].mean().reset_index()
            x = messages_df['date'].values.tolist()
        else:
            messages_df = self.messages_df
            x = list(range(len(self.messages_df)))
        charts_data = []
        for column in included_columns:
            chart = {
                "x": x,
                "y": messages_df[column].values.tolist(),
                "mode": "lines+markers",
                "name": column,
            }
            charts_data.append(chart)

        return {
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
