from abc import ABC, abstractmethod

from database import BaseDatabaseHandler
from loaders.channels import BaseChannelsLoader
from loaders.accounts import BaseAccountsLoader
from scraper.managers import ChannelsManager, MessagesManager


class BaseScraper(ABC):
    def __init__(self, channels_loader: BaseChannelsLoader, accounts_loader: BaseAccountsLoader,
                 db_handler: BaseDatabaseHandler):
        self.channels_loader = channels_loader
        self.accounts_loader = accounts_loader
        self.db_handler = db_handler
        self.channels_manager = None
        self.messages_manager = None

    def set_channels_manager(self, client):
        self.channels_manager = ChannelsManager(client=client, channels_loader_adaptor=self.channels_loader)

    def set_messages_manager(self, client):
        self.messages_manager = MessagesManager(client=client)

    @abstractmethod
    def run_scraper(self):
        pass
