import logging
from io import BytesIO
import base64

from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from pandas import DataFrame
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud

from web_app.components.utils.basic_components import generate_section_banner
from .base_dashboard_component import BaseDashboardComponent
from utils import stopwords_custom_languages, custom_stopwords, clean_text_from_stopwords

logger = logging.getLogger(__name__)
nltk.download('stopwords')


class MessageWordCloudChartsComponent(BaseDashboardComponent):
    MOST_RECENT_MESSAGE_OFFSET = 3
    DEFAULT_STOPWORDS_LANGUAGES = ['english', 'ukrainian']
    LANGUAGES_OPTIONS = stopwords_custom_languages + stopwords.fileids()

    def set_messages_df(self, messages_df: DataFrame):
        super().set_messages_df(messages_df)
        self.messages_df = self.messages_df[:-self.MOST_RECENT_MESSAGE_OFFSET]

    def build(self):
        return html.Div(
            className='control-chart-container',
            children=[
                generate_section_banner('WordCloud form all messages'),
                self.build_interacted_components(),
                html.Img(id="image_messages_wc", className='wc-image')
            ],
        )

    def set_callbacks(self):
        callback(
            Output('image_messages_wc', 'src'),
            [Input('build-messages-wc', 'n_clicks')],
            [State('wc-languages-dropdown', 'value')]
            # background=True
        )(self.build_wc_image)

    def build_interacted_components(self):
        return html.Div(
            [
                dcc.Loading(
                    id='loading-messages-wc',
                    type='circle',
                    children=[
                        dbc.Button(
                            id='build-messages-wc',
                            children='Build', n_clicks=0, outline=True,
                            className='btn-build',
                        ),
                        html.Div(id='loading-messages-wc-output')
                    ],
                ),
                dcc.Dropdown(
                    self.LANGUAGES_OPTIONS, self.DEFAULT_STOPWORDS_LANGUAGES,
                    id='wc-languages-dropdown',
                    multi=True,
                    className='wc-languages-dropdown',
                    placeholder='Select stopwords languages'
                )
            ],
            className='wc_interacted_container',
        )

    def build_wc_image(self, n_clicks, needed_languages):
        img = BytesIO()

        all_stopwords = []
        nltk_languages = stopwords.fileids()

        for lang in needed_languages:
            if lang in nltk_languages:
                all_stopwords.extend(stopwords.words(lang))
            else:
                all_stopwords.extend(custom_stopwords(lang))

        messages_df = self.messages_df.copy()
        messages_df['message_nostop'] = messages_df['message'].apply(lambda x: clean_text_from_stopwords(x.lower(),
                                                                                                         all_stopwords))
        full_text_from_messages = "".join(messages_df['message_nostop'].tolist())

        messages_wordcloud = WordCloud(background_color=(22, 26, 40), width=800, height=800).generate(full_text_from_messages)

        messages_wordcloud.to_image().save(img, format='PNG')

        return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
