import logging

from telethon.tl.patched import Message, MessageService

from loaders.channels import BaseChannelsLoader
from managers import ChannelsManager, MessagesManager
from .base_worker import BaseWorker

logger = logging.getLogger(__name__)


class ChannelsScraper(BaseWorker):
    MESSAGES_LIMIT = 1
    COMMENTS_LIMIT = 100

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

        for channel in channels:
            logger.info(f"Start scraping from channel({channel.title}/{channel.id})")
            messages_ids = await self.scrape_and_store_messages_from_channel(channel)
            await self.scrape_and_store_comments_to_message(channel, messages_ids)

    # TODO: add logic for last_message_id because we wanna get messages starting from from already grabbed
    async def scrape_and_store_messages_from_channel(self, channel, last_message_id=None):
        messages_ids = []
        async for messages_chunk in self.get_messages(channel):
            for message in messages_chunk:
                messages_ids.append(message.id)
                logger.info(message.to_dict())
            # TODO: result = await self.storage_adapter.save_messages(messages_chunk)
        if not messages_ids:
            logger.warning("No messages")
        return messages_ids

    # TODO: add logic for last_comment_id because we wanna get comments starting from already grabbed
    async def scrape_and_store_comments_to_message(self, channel, messages_ids, last_comment_id=None):
        for message_id in messages_ids:
            async for comments_chunk in self.get_comments_to_message(channel, message_id):
                logger.info(comments_chunk)
                # TODO: result = await self.storage_adapter.save_comments(comments_chunk)

    def get_messages(self, channel):
        return self.messages_manager.iter_messages(channel, self.MESSAGES_LIMIT, 0)

    def get_comments_to_message(self, channel, message_id):
        return self.messages_manager.iter_messages(channel=channel, limit=self.COMMENTS_LIMIT, reply_to=message_id)
