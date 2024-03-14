import logging

from .auth_scraper import AuthScraper
from utils import settings

logger = logging.getLogger(__name__)


class Scraper(AuthScraper):
    MESSAGES_LIMIT = settings.TELEGRAM_MESSAGES_SCRAPING_LIMIT
    COMMENTS_LIMIT = settings.TELEGRAM_COMMENTS_SCRAPING_LIMIT

    async def start_scraping(self, channel_id: int) -> None:
        channels = await self.channels_manager.get_channels()

        for channel in channels:
            if channel_id and channel_id != channel.id:
                continue
            logger.info(f"Start scraping from channel({channel.title}/{channel.id})")
            self.scrape_and_store_channel_info(channel)
            await self.scrape_and_store_messages_from_channel(channel)

    def scrape_and_store_channel_info(self, channel):
        self.db_handler.store_channel(channel.id, channel.title, channel.to_json())

    # TODO: add logic for last_message_id because we wanna get messages starting from already grabbed
    async def scrape_and_store_messages_from_channel(self, channel):
        async for messages_chunk in self.get_messages(channel):
            for message in messages_chunk:
                self.db_handler.store_message(channel.id, message.id, message.to_json())
                await self.scrape_and_store_comments_to_message(channel, message.id)

    async def scrape_and_store_comments_to_message(self, channel, message_id):
        async for comments_chunk in self.get_comments_to_message(channel, message_id):
            for comment in comments_chunk:
                self.db_handler.store_comment(channel.id, message_id, comment.id, comment.to_json())

    def get_messages(self, channel):
        return self.messages_manager.iter_messages(channel, self.MESSAGES_LIMIT, 0)

    def get_comments_to_message(self, channel, message_id):
        return self.messages_manager.iter_messages(channel=channel, limit=self.COMMENTS_LIMIT, reply_to=message_id)
