from typing import Generator, List
import logging

from telethon.tl import functions, types
from telethon.tl.patched import Message, MessageService
from telethon import tl

logger = logging.getLogger(__name__)


class MessagesManager:
    POSTS_PER_REQUEST_LIMIT = 100

    def __init__(self, client):
        self.client = client
        self.user_owner = self.client.get_me()

    async def iter_messages(self, channel, limit=10, offset_msg_id=0, reply_to=None) -> Generator[List[Message], None, None]:
        """
        Get (limit) number of messages from channel.

        :returns tl.types.messages.Messages: Instance of either Messages, MessagesSlice, ChannelMessages, MessagesNotModified.
        """
        total_messages = 0

        while total_messages < limit:
            try:
                messages = await self.client.get_messages(
                    channel,
                    offset_id=offset_msg_id,
                    limit=self.POSTS_PER_REQUEST_LIMIT,
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

    async def get_discussion_message(self, channel_id, message_id) -> tl.types.messages.DiscussionMessage or None:
        """
        If channel have discussion chat some messages gonna have they room in this chat,
        so we cat get discussion object for this message(post)
        """
        try:
            discussion_msg = await self.client(
                functions.messages.GetDiscussionMessageRequest(peer=channel_id,
                                                               msg_id=message_id))
            return discussion_msg
        except Exception as e:
            logger.warning(e)
        return
