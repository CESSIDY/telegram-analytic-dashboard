from abc import ABC, abstractmethod

from dash import html, dcc

from database import BaseDatabaseHandler
from loaders.channels import BaseChannelsLoader


class BaseComponent(ABC):
    def __init__(self, db_handler: BaseDatabaseHandler, channels_loader: BaseChannelsLoader):
        self.db_handler = db_handler
        self.channels_loader = channels_loader

    @abstractmethod
    def build(self):
        pass
