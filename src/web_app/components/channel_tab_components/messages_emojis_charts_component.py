import logging

from dash import html, dcc, callback, Output, Input, State, Patch, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from pandas import DataFrame
import numpy as np

from services import DBDataToPandasLoader
from web_app.components.utils.basic_components import generate_section_banner
from .base_dashboard_component import BaseDashboardComponent

logger = logging.getLogger(__name__)


class MessageEmojisChartsComponent(BaseDashboardComponent):
    MOST_RECENT_MESSAGE_OFFSET = 3
    DEFAULT_COLORS = ['skyblue', 'green', 'orange', 'white', 'purple', 'azure',
                      'chocolate', 'coral', 'darkgrey', 'darkviolet']
    TITLE_FONT_COLOR = 'rgb(30,125,125)'
    TITLE_FONT_SIZE = 20
    TICK_FONT_COLOR = 'darkgray'
    TICK_FONT_SIZE = 15

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
            className='control-chart-container',
            children=[
                generate_section_banner('Distribution of messages broken down by main reactions'),
                self.build_interacted_components(),
                html.Div([
                    dcc.Graph(
                        id='message-emojis-linechart',
                        figure=self.build_linechart_figure()
                    ),
                    dcc.Graph(
                        id='message-emojis-piechart',
                        figure=self.build_chart_figure()
                    )
                ], className='emojis-all-graph-container')
            ],
        )

    def set_callbacks(self):
        callback(
            [Output('message-emojis-piechart', 'figure'),
             Output('message-emojis-linechart', 'figure'),
             Output('loading-message-emojis-charts-output', 'children')],
            [Input('build-message-emojis-charts', 'n_clicks')],
            [State({'type': 'emojis-group-name', 'index': ALL}, 'value'),
             State({'type': 'emojis-group-dropdown', 'index': ALL}, 'value')],
            prevent_initial_call=True
            # background=True
        )(self.build_chart_figure_callback)
        callback(
            Output('emojis-dropdown-container-div', 'children'),
            Input('add-emojis-group-btn', 'n_clicks')
            # background=True
        )(self.display_dropdowns)

    def build_chart_figure_callback(self, n_clicks, emojis_groups_names, emojis_groups_dropdowns):
        if n_clicks <= 0:
            raise PreventUpdate

        return (self.build_chart_figure(emojis_groups_names, emojis_groups_dropdowns),
                self.build_linechart_figure(emojis_groups_names, emojis_groups_dropdowns),
                None)

    def build_interacted_components(self):
        return html.Div(
            [
                html.Div(
                    [
                        html.Button('Add group', id='add-emojis-group-btn', n_clicks=0,
                                    style={'display': 'flex'}),
                        dcc.Loading(
                            id='loading-message-emojis-charts',
                            type='circle',  # or default
                            children=[
                                dbc.Button(
                                    id='build-message-emojis-charts',
                                    children='Build', n_clicks=0, outline=True,
                                    className='btn-build',
                                ),
                                html.Div(id='loading-message-emojis-charts-output')
                            ],
                        )
                    ],
                    className='btn-group'
                ),
                html.Div(
                    id='emojis-dropdown-container-div',
                    children=[],
                    style={'display': 'flex', 'gap': '10px', 'flex-wrap': 'wrap'}
                ),
            ],
            className='emoji_interacted_container',
        )

    def display_dropdowns(self, n_clicks):
        if n_clicks <= 0:
            raise PreventUpdate
        patched_children = Patch()
        new_dropdown = html.Div([
                dcc.Input(
                    id={"type": 'emojis-group-name', 'index': n_clicks},
                    placeholder='Enter group name',
                    type='text',
                    style={'display': 'flex'}
                ),
                dcc.Dropdown(
                    self.all_emojis_options, [],
                    id={"type": 'emojis-group-dropdown', 'index': n_clicks},
                    multi=True,
                )
            ],
            style={'display': 'flex', 'flex-direction': 'column', 'gap': '5px'}
        )
        patched_children.append(new_dropdown)
        return patched_children

    def build_chart_figure(self, emojis_groups_names=(), emojis_groups_dropdowns=()):
        categories = {}

        if not emojis_groups_names and not emojis_groups_dropdowns:
            emojis_groups_dropdowns = [self.all_emojis_options]
            emojis_groups_names = ["ALL"]

        for group_name, emojis in zip(emojis_groups_names, emojis_groups_dropdowns):
            categories[group_name] = emojis

        messages_df = self.messages_df.copy()
        messages_df['category'] = self.messages_df['main_emoji_reaction'].map(
            {v: k for k, values in categories.items() for v in values})
        grouped_by_categories_df = messages_df.groupby(['category'])['id'].count().reset_index()
        categories_count = grouped_by_categories_df['id']
        labels = grouped_by_categories_df['category']

        colors = self.DEFAULT_COLORS
        if len(self.DEFAULT_COLORS) > len(labels):
            colors = self.DEFAULT_COLORS[:len(labels)]
        elif len(self.DEFAULT_COLORS) < len(labels):
            colors = [self.DEFAULT_COLORS[i % len(self.DEFAULT_COLORS)] for i in range(len(labels))]

        pie_plot = go.Pie(labels=labels, values=categories_count, marker=dict(colors=colors))

        layout = {
            'margin': dict(l=20, r=20, t=20, b=20),
            'showlegend': True,
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {"color": self.TITLE_FONT_COLOR, "size": self.TITLE_FONT_SIZE},
            "legend": {"font": {"size": self.TICK_FONT_SIZE, "color": self.TICK_FONT_COLOR}},
            'autosize': True,
        }

        fig = go.Figure(data=[pie_plot], layout=layout)

        return fig

    def build_linechart_figure(self, emojis_groups_names=(), emojis_groups_dropdowns=()):
        categories = {}

        if not emojis_groups_names and not emojis_groups_dropdowns:
            emojis_groups_dropdowns = [self.all_emojis_options]
            emojis_groups_names = ["ALL"]

        for group_name, emojis in zip(emojis_groups_names, emojis_groups_dropdowns):
            categories[group_name] = emojis

        messages_df: DataFrame = self.messages_df.copy()
        messages_df['category'] = self.messages_df['main_emoji_reaction'].map(
            {v: k for k, values in categories.items() for v in values})

        messages_df = messages_df.groupby(['date', 'category'])['id'].count().reset_index()
        messages_df.rename({'id': 'count'}, axis=1, inplace=True)

        # TODO: Check sorting
        dates = messages_df.sort_values(by='date', ascending=False)['date'].unique()
        data = {category: [0] * len(dates) for category in categories.keys()}
        new_df = DataFrame({'date': dates, **data})

        for date in list(dates):
            current_date_messages = messages_df[messages_df['date'] == date]
            for category in categories.keys():
                current_category_messages = current_date_messages[current_date_messages['category'] == category]
                if not current_category_messages.empty:
                    new_df.loc[new_df['date'] == date, category] = current_category_messages['count'].values[0]
        charts_data = []
        annotations = []
        for i, category in enumerate(categories.keys()):
            current_color_index = i % len(self.DEFAULT_COLORS)
            y = new_df[category].values.tolist()
            mean_y = np.mean(y)
            mean_y_formatted = '{:,.0f}'.format(int(mean_y))
            mean_line_y = [mean_y] * len(dates)
            chart = go.Scatter(x=dates, y=new_df[category], mode='lines+markers', name=category,
                               line={'color': self.DEFAULT_COLORS[current_color_index]})
            mean_line = go.Scatter(x=dates, y=mean_line_y, mode='lines', name=f'{category}-mean',
                                   line={"color": self.DEFAULT_COLORS[current_color_index], "dash": "dash"})
            annotation = go.Annotation(x=dates[0], y=mean_y, text=f" {mean_y_formatted}", showarrow=False,
                                       xanchor='left', yanchor='middle', valign='middle', xref='x', yref='y',
                                       align='left', font={"color": self.DEFAULT_COLORS[current_color_index],
                                                           "size": self.TICK_FONT_SIZE})
            charts_data.append(chart)
            charts_data.append(mean_line)
            annotations.append(annotation)

        layout = {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "xaxis": {
                "title": "Date",
                "zeroline": False,
                "showgrid": False,
                "showline": False,
                "tickfont": {"size": self.TICK_FONT_SIZE, "color": self.TICK_FONT_COLOR},
                "titlefont": {"color": self.TITLE_FONT_COLOR, "size": self.TITLE_FONT_SIZE},
            },
            "yaxis": {
                "title": 'Messages count',
                "showgrid": False,
                "showline": False,
                "zeroline": False,
                "tickfont": {"size": self.TICK_FONT_SIZE, "color": self.TICK_FONT_COLOR},
                "titlefont": {"color": self.TITLE_FONT_COLOR, "size": self.TITLE_FONT_SIZE},
            },
            "legend": {"font": {"size": self.TICK_FONT_SIZE, "color": self.TICK_FONT_COLOR}},
            "autosize": True,
            "annotations": annotations
        }

        fig = go.Figure(data=charts_data, layout=layout)

        return fig
