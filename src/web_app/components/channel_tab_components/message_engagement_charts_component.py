import logging

from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from pandas import DataFrame
import numpy as np

from web_app.components.utils.basic_components import generate_section_banner
from .base_dashboard_component import BaseDashboardComponent

logger = logging.getLogger(__name__)


class MessageEngagementChartsComponent(BaseDashboardComponent):
    MOST_RECENT_MESSAGE_OFFSET = 3  # TODO: Remove just messages for N last days (give user to decide)
    DEFAULT_INCLUDED_COLUMNS = ['views', 'forwards', 'reactions']
    DEFAULT_COLORS = ['skyblue', 'green', 'red', 'orange', 'purple']  # Define custom colors for lines

    def set_messages_df(self, messages_df: DataFrame):
        super().set_messages_df(messages_df)
        self.messages_df = self.messages_df[:-self.MOST_RECENT_MESSAGE_OFFSET]

    def build(self):
        return html.Div(
            className='control-chart-container',
            children=[
                generate_section_banner('Message Engagement Trends Over Time'),
                self.build_interacted_components(),
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='message-engagement-linechart',
                            figure=go.Figure(self.build_chart_figure()),
                            className='message-engagement-linechart'
                        ),
                        dcc.Graph(
                            id='messages-count-linechart',
                            figure=go.Figure(self.build_messages_count_chart_figure()),
                            className='messages-count-linechart'
                        ),
                    ], className='message-engagement-two-graph-container'),
                    dcc.Graph(
                        id='users-actions-by-month-barchart',
                        figure=go.Figure(self.build_user_actions_by_month_chart_figure()),
                        className='users-actions-by-month-barchart',
                    )
                ], className='message-engagement-all-graph-container')
            ],
        )

    def set_callbacks(self):
        callback(
            [Output('message-engagement-linechart', 'figure'),
             Output('messages-count-linechart', 'figure'),
             Output('users-actions-by-month-barchart', 'figure'),
             Output('loading-message-engagement-charts-output', 'children'),
             ],
            [Input('build-message-engagement-charts', 'n_clicks')
             ],
            [State('chart-panel-columns-checklist', 'value'),
             State('chart-panel-group-by-date', 'value')
             ],
            # background=True
        )(self.build_chart_figure_callback)

    def build_chart_figure_callback(self, n_click, included_columns, is_group_by_date):
        return (self.build_chart_figure(n_click, included_columns, is_group_by_date),
                self.build_messages_count_chart_figure(n_click),
                self.build_user_actions_by_month_chart_figure(n_click, included_columns),
                None)

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
            x_column_title = 'Date'
        else:
            messages_df = self.messages_df
            x = list(range(len(self.messages_df)))
            x_column_title = 'Message'
        charts_data = []
        for i, column in enumerate(included_columns):
            y = messages_df[column].values.tolist()
            mean_y = np.mean(y)
            mean_line = [mean_y] * len(x)
            chart = {
                "x": x,
                "y": y,
                "mode": "lines+markers",
                "name": column,
                "line": {"color": self.DEFAULT_COLORS[i]}
            }
            mean_line = {
                "x": x,
                "y": mean_line,
                "mode": "lines",
                "name": f"{column}-mean",
                "line": {"color": self.DEFAULT_COLORS[i], "dash": "dash"}
            }
            charts_data.append(chart)
            charts_data.append(mean_line)

        return {
            "data": charts_data,
            "layout": {
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "xaxis": {
                    "zeroline": False,
                    "showgrid": False,
                    "title": x_column_title,
                    "showline": False,
                    #"domain": [0, 0.8],
                    "titlefont": {"color": "darkgray"},
                },
                "yaxis": {
                    "title": 'Users count',
                    "showgrid": False,
                    "showline": False,
                    "zeroline": False,
                    "titlefont": {"color": "darkgray"},
                },
                "autosize": True,
            },
        }

    def build_messages_count_chart_figure(self, n_click=1):
        if n_click <= 0:
            raise PreventUpdate

        messages_df = self.messages_df.groupby(['date'])['id'].count().reset_index()
        messages_df.rename({'id': 'count'}, axis=1, inplace=True)

        return {
            "data": [{
                "x": messages_df['date'].tolist(),
                "y": messages_df['count'].tolist(),
                "mode": "lines+markers",
                "name": 'Messages count per day',
            }],
            "layout": {
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "xaxis": {
                    "zeroline": False,
                    "showgrid": False,
                    "title": "Date",
                    "showline": False,
                    #"domain": [0, 0.8],
                    "titlefont": {"color": "darkgray"},
                },
                "yaxis": {
                    "title": 'Message count',
                    "showgrid": False,
                    "showline": False,
                    "zeroline": False,
                    "titlefont": {"color": "darkgray"},
                },
                "autosize": True,
            },
        }

    def build_user_actions_by_month_chart_figure(self, n_click=1, included_columns=None):
        if not included_columns:
            included_columns = self.DEFAULT_INCLUDED_COLUMNS

        messages_df = self.messages_df.groupby(['month'])[list(included_columns)].sum().reset_index()
        df_melted = messages_df.melt(id_vars=['month'], value_vars=list(included_columns), var_name='actions',
                                     value_name='users_count')

        ####################
        unique_actions = df_melted['actions'].unique()
        charts_data=[]
        for i, action in enumerate(unique_actions):
            filtered_df = df_melted[df_melted['actions'] == action]

            charts_data.append({
                "x": filtered_df['users_count'].tolist(),
                "y": filtered_df['month'].tolist(),
                "orientation": "h",
                "name": action,
                "type": "bar"
            })

        return {
            "data": charts_data,
            "layout": {
                "barmode": "group",  #stack
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "xaxis": {
                    "zeroline": False,
                    "showgrid": False,
                    "title": "Actions count",
                    "showline": False,
                    # "domain": [0, 0.8],
                    "titlefont": {"color": "darkgray"},
                },
                "yaxis": {
                    "title": 'Month',
                    "showgrid": False,
                    "showline": False,
                    "zeroline": False,
                    "titlefont": {"color": "darkgray"},
                },
                "autosize": True,
            },
        }
