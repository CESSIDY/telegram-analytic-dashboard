import logging

from dash import html, dcc, callback, Output, Input, State, Patch, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from pandas import DataFrame

from services import DBDataToPandasLoader
from web_app.components.utils.basic_components import generate_section_banner
from .base_dashboard_component import BaseDashboardComponent

logger = logging.getLogger(__name__)


class MessageEmojisChartsComponent(BaseDashboardComponent):
    MOST_RECENT_MESSAGE_OFFSET = 3

    def __init__(self):
        super().__init__()
        self.all_emojis_options = []

    def set_messages_df(self, messages_df: DataFrame):
        super().set_messages_df(messages_df)
        self.messages_df = self.messages_df[:-self.MOST_RECENT_MESSAGE_OFFSET]

    def set_db_data_to_pandas_loader(self, db_data_to_pandas_loader: DBDataToPandasLoader):
        super().set_db_data_to_pandas_loader(db_data_to_pandas_loader)
        self.all_emojis_options = list(self.db_data_to_pandas_loader.get_all_emojis_reactions_in_channel(self.channel_id))

    def build(self):
        return html.Div(
            id="piechart-container-outer",
            className="twelve columns",
            children=[
                generate_section_banner("Distribution of messages broken down by main reactions"),
                self.build_interacted_components(),
                dcc.Graph(
                    id="message-emojis-linechart",
                    figure=go.Figure(self.build_chart_figure())
                )
            ],
        )

    def set_callbacks(self):
        callback(
            [Output('message-emojis-linechart', 'figure'),
             Output('loading-message-emojis-charts-output', 'children')],
            [Input("build-message-emojis-charts", "n_clicks")],
            [State({"type": "emojis-group-name", "index": ALL}, "value"),
             State({"type": "emojis-group-dropdown", "index": ALL}, "value")],
            prevent_initial_call=True
            # background=True
        )(self.build_chart_figure_callback)
        callback(
            Output("emojis-dropdown-container-div", "children"),
            Input("add-emojis-group-btn", "n_clicks")
            # background=True
        )(self.display_dropdowns)

    def build_chart_figure_callback(self, n_click, emojis_groups_names, emojis_groups_dropdowns):
        return self.build_chart_figure(n_click, emojis_groups_names, emojis_groups_dropdowns), None

    def build_interacted_components(self):
        return html.Div(
            [
                html.P(
                    [
                        html.Button("Add group", id="add-emojis-group-btn", n_clicks=0,
                                    style={'display': 'inline-block', 'margin': '5px', 'width': '100%'}),
                        dcc.Loading(
                            id='loading-message-emojis-charts',
                            type='circle',  # or default
                            children=[
                                dbc.Button(
                                    id='build-message-emojis-charts',
                                    children='Build', n_clicks=0, outline=True,
                                    style={'display': 'inline-block', 'margin': '5px', 'width': '100%'}
                                ),
                                html.Div(id='loading-message-emojis-charts-output')
                            ],
                        )
                    ],
                    style={'display': 'inline-block', 'margin-left': '20px', 'margin-right': '20px',
                           'vertical-align': 'middle'}
                ),
                html.Div([
                    html.Div(
                        [
                            html.Div(id="emojis-dropdown-container-div", children=[]),
                        ],
                        style={'display': 'inline-block', 'margin-right': '10px', 'margin-left': '10px'}
                    )],
                    style={'display': 'inline-block', 'vertical-align': 'middle'}
                ),
            ],
            className='auto__container',
        )

    def display_dropdowns(self, n_clicks):
        if n_clicks <= 0:
            raise PreventUpdate
        patched_children = Patch()
        new_dropdown = html.Div([
                dcc.Input(id={"type": "emojis-group-name", "index": n_clicks}, placeholder='Enter group name',
                          type='text', style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '10px', 'max-width': '150px'}),
                dcc.Dropdown(
                    self.all_emojis_options, [],
                    id={"type": "emojis-group-dropdown", "index": n_clicks},
                    multi=True,
                    style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '10px', 'min-width': '100px'}
                )
            ], className='auto__container', style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-right': '10px'}
        )
        patched_children.append(new_dropdown)
        return patched_children

    def build_chart_figure(self, n_clicks=1, emojis_groups_names=(), emojis_groups_dropdowns=()):
        if n_clicks <= 0:
            raise PreventUpdate

        categories = {}

        if not emojis_groups_names and not emojis_groups_dropdowns:
            emojis_groups_dropdowns = self.all_emojis_options
            emojis_groups_names = ["ALL"]

        for group_name, emojis in zip(emojis_groups_names, emojis_groups_dropdowns):
            categories[group_name] = emojis

        messages_df = self.messages_df.copy()
        messages_df['category'] = self.messages_df['main_emoji_reaction'].map(
            {v: k for k, values in categories.items() for v in values})
        grouped_by_categories_df = messages_df.groupby(['category'])['id'].count().reset_index()
        categories_count = grouped_by_categories_df['id']
        labels = grouped_by_categories_df['category']

        # plt.pie(categories_count, labels=labels, autopct='%1.1f%%', startangle=90)

        return {
            "data": [go.Pie(labels=labels, values=categories_count)],
            "layout": {
                "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True,
            }
        }
