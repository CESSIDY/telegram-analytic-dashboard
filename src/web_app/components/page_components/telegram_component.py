import logging
import functools

from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate

from scraper import Scraper
from .base_component import BaseComponent

logger = logging.getLogger(__name__)


def lock_per_process(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        self.ONE_PROCESS_AT_TIME_LOCK = True
        result = func(*args, **kwargs)
        self.ONE_PROCESS_AT_TIME_LOCK = False
        return result

    return wrapper


class TelegramComponent(BaseComponent):

    ONE_PROCESS_AT_TIME_LOCK = False

    def __init__(self, scraper: Scraper):
        self.scraper = scraper

    def build(self):
        pass

    def is_scraper_unlocked(self):
        return not self.ONE_PROCESS_AT_TIME_LOCK

    @lock_per_process
    def run_scraping(self, channel_id=None):
        self.scraper.run_scraper(channel_id)

    @lock_per_process
    def client_connect(self):
        self.scraper.client_connect()

    @lock_per_process
    def client_disconnect(self):
        self.scraper.client_disconnect()

    @lock_per_process
    def is_authorized(self) -> bool:
        return self.scraper.is_user_authorized()

    @lock_per_process
    def send_code_request(self):
        self.scraper.send_code_request()

    @lock_per_process
    def sign_in(self, code: int):
        try:
            self.scraper.sign_in(code)
        except Exception as e:
            return False, e
        return True, ""

