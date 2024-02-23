import logging

from telethon.tl.patched import Message, MessageService

from loaders.channels import BaseChannelsLoader
from managers import ChannelsManager, MessagesManager
from .base_worker import BaseWorker

logger = logging.getLogger(__name__)


class ChannelsScraper(BaseWorker):
    MAX_SCRAPER_POSTS = 10

    def __init__(self, client, channels_loader_adaptor: BaseChannelsLoader, storage_adapter):
        self.channels_loader = channels_loader_adaptor
        self.storage_adapter = storage_adapter
        self.client = client
        self.channels_manager = ChannelsManager(client=self.client, channels_loader_adaptor=self.channels_loader)
        self.messages_manager = MessagesManager(client=self.client)

    def run_until_complete(self):
        with self.client:
            self.client.loop.run_until_complete(self.start_scraping())

    async def start_scraping(self):
        channels = await self.channels_manager.get_channels()
        for channel in await channels:
            logger.info(f"Start scraping from channel({channel.title}/{channel.id})")
            async for channel_data_chunk in self.messages_manager.iter_messages(channel, self.MAX_SCRAPER_POSTS, 0):
                for message in channel_data_chunk:
                    logger.info(message.to_dict())
                # result = await self.storage_adapter.save_channel_data(channel_data_chunk)
                # TODO
