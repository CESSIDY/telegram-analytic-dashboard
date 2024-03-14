import logging
import threading
import asyncio

from telethon.sync import TelegramClient

from .base_scraper import BaseScraper
from scraper.utils import get_session_path
from utils import get_proxy_configurations, configure_logging, settings

configure_logging()
logger = logging.getLogger(__name__)


class AuthScraper(BaseScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_client = None
        self.phone_code_hash = None

    @property
    def client(self):
        if not self.current_client:
            self.set_current_client()
            self.client_connect()
        return self.current_client

    def run_scraper(self, channel_id: int = None):
        self.client_disconnect()
        del self.current_client
        scraper_thread = threading.Thread(target=self._run_scraper_at_thread, args=(channel_id,))
        scraper_thread.start()
        scraper_thread.join()

    def _run_scraper_at_thread(self, channel_id: int):
        self._check_on_event_loop()
        self.set_current_client()
        self.authenticate()
        self.run_channels_scraper(channel_id)

    @staticmethod
    def _check_on_event_loop():
        try:
            _ = asyncio.get_event_loop()
        except RuntimeError as e:
            if str(e).startswith('There is no current event loop in thread'):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            else:
                raise

    def authenticate(self):
        self.init_session()

    def init_session(self):
        logger.info(f"Try login for: {settings.TELEGRAM_USERNAME}")
        try:
            with self.client:
                pass
            logger.info(f"Login successfully: {settings.TELEGRAM_USERNAME}")
        except Exception as err:
            logger.error(f"Authorization error for {settings.TELEGRAM_USERNAME}")
            raise err

    def set_current_client(self):
        session_path = get_session_path(settings.TELEGRAM_USERNAME)
        logger.info(f"Session path: {session_path}")

        proxy = get_proxy_configurations()
        if proxy:
            client = TelegramClient(session_path, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH, proxy=proxy)
        else:
            client = TelegramClient(session_path, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)

        self.current_client = client

    def client_connect(self):
        self.client.connect()
        logger.info("Client connected")

    def client_disconnect(self):
        self.client.disconnect()
        logger.info("Client disconnect")

    def is_user_authorized(self):
        me = self.client.get_me()
        return bool(me is not None)

    def send_code_request(self):
        result = self.client.send_code_request(settings.TELEGRAM_PHONE)
        if result:
            self.phone_code_hash = result.phone_code_hash
        logger.info(f"Send code request")

    def sign_in(self, code: int):
        self.client.sign_in(phone=settings.TELEGRAM_PHONE, code=code, phone_code_hash=self.phone_code_hash)
        logger.info("Login successful")

    def run_channels_scraper(self, channel_id: int):
        with self.client:
            self.set_channels_manager(self.client)
            self.set_messages_manager(self.client)
            self.client.loop.run_until_complete(self.start_scraping(channel_id))

    async def start_scraping(self, channel_id: int):
        pass
