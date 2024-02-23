from src.loaders.channels import BaseChannelsLoader
from src.managers import ChannelsManager
import logging
from .base_worker import BaseWorker

logger = logging.getLogger(__name__)


class ChannelsScraper(BaseWorker):
    def __init__(self, client, channels_loader_adaptor: BaseChannelsLoader, scraper_adapter, storage_adapter):
        self.channels_loader = channels_loader_adaptor
        self.scraper_adapter = scraper_adapter
        self.storage_adapter = storage_adapter
        self.client = client
        self.channels_manager = ChannelsManager(client=self.client, channels_loader_adaptor=self.channels_loader)

    def run_until_complete(self):
        with self.client:
            self.client.loop.run_until_complete(self.start_scraping())

    async def start_scraping(self):
        channels = await self.channels_manager.get_channels()
        for channel in await channels:
            logger.info(f"Start scraping from channel({channel.title}/{channel.id})")
            for channel_data_chunk in await self.scraper_adapter.scrape_channel(channel):
                result = await self.storage_adapter.save_channel_data(channel_data_chunk)
                # TODO
