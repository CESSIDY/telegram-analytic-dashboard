from typing import Generator, List
import logging

from telethon.tl import functions, types
from telethon.tl.patched import Message, MessageService
from telethon import tl

logger = logging.getLogger(__name__)


class MessagesManager:
    MESSAGES_PER_REQUEST_LIMIT = 100

    def __init__(self, client):
        self.client = client
        self.user_owner = self.client.get_me()

    async def iter_messages(self, channel, limit=10, offset_msg_id=0, reply_to=None) -> Generator[List[Message], None, None]:
        total_messages = 0
        while total_messages < limit:
            try:
                messages = await self.client.get_messages(
                    channel,
                    offset_id=offset_msg_id,
                    limit=self.MESSAGES_PER_REQUEST_LIMIT if limit > self.MESSAGES_PER_REQUEST_LIMIT else limit,
                    reply_to=reply_to,
                )
                if not messages:
                    break
            except Exception as e:
                logger.error(e)
                yield []
                return

            offset_msg_id = messages[len(messages) - 1].id
            total_messages += len(messages)

            yield messages
