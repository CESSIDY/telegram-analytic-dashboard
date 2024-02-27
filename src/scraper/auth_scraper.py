import logging

from telethon.sync import TelegramClient

from .base_scraper import BaseScraper
from models import AccountsLoaderModel
from scraper.utils import get_session_path
from utils import get_proxy_configurations, configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class AuthScraper(BaseScraper):
    def run_scraper(self):
        clients = self.authenticate()
        self.run_channels_scraper_for_each_account(clients)

    def authenticate(self):
        account_models = self.accounts_loader.get_all()
        accounts_models = self.init_sessions(account_models)
        return accounts_models

    def init_sessions(self, account_models: [AccountsLoaderModel]) -> [TelegramClient]:
        valid_clients = list()

        for account in account_models:
            print(f"Login for: {account.username}")
            try:
                client = self.get_client(account)
                with client:
                    pass  # just for creating session files
                valid_clients.append(client)
            except Exception as err:
                print(f"Authorization error for {account.username}")
                logger.error(err)

        return valid_clients

    @staticmethod
    def get_client(account_model: AccountsLoaderModel):
        session_path = get_session_path(account_model.username)
        logger.info(f"Session path: {session_path}")

        proxy = get_proxy_configurations()
        if proxy:
            client = TelegramClient(session_path, account_model.api_id, account_model.api_hash, proxy=proxy)
        else:
            client = TelegramClient(session_path, account_model.api_id, account_model.api_hash)

        return client

    def run_channels_scraper_for_each_account(self, clients: [TelegramClient]):
        for client in clients:
            with client:
                self.set_channels_manager(client)
                self.set_messages_manager(client)
                client.loop.run_until_complete(self.start_scraping())

    async def start_scraping(self):
        pass
