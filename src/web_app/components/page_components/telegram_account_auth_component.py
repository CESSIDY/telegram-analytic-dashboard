import logging
import functools

from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate

from scraper import Scraper
from .base_component import BaseComponent
from .telegram_component import TelegramComponent


logger = logging.getLogger(__name__)


class TelegramAccountAuthComponent(TelegramComponent):

    def __init__(self, *args, main_app_component: BaseComponent, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_app_component = main_app_component
        self.set_callbacks()

    def build(self):
        self.send_code_request()
        return self.build_enter_code_window()

    def set_callbacks(self):
        callback(
            Output("main-app-component", "children", allow_duplicate=True),
            [Input("auth-login-button", "n_clicks")],
            [State("auth-code-field-input", "value")],
            background=True,
            prevent_initial_call=True,
        )(self.check_auth_code_input)

    def check_auth_code_input(self, n_clicks, value: int):
        if not n_clicks or n_clicks <= 0:
            raise PreventUpdate
        is_sing_in, exception = self.sign_in(value)
        if is_sing_in:
            return self.main_app_component.build()
        return self.build_enter_code_window(str(exception))

    @staticmethod
    def build_enter_code_window(exception=None):
        return html.Div(children=[
            html.Div(children=[
                html.Label("Before starting scraping, you need to authorize, enter the code received from telegram and run scraping again", className="auth-label"),
                html.Label(exception, className="exception-label"),
                html.Div(children=[
                    dcc.Input(id="auth-code-field-input", className='auth-code-field-input',
                              placeholder='Enter the code you received', type='number'),
                    html.Button('Login', id="auth-login-button", className='auth-login-button', n_clicks=0)
                ],
                    className="enter-auth-code-form"
                ),
            ], className="auth-main")
        ], className="auth-window")
