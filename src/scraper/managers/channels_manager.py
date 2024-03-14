import logging
from typing import List

from telethon.tl import functions, types
from telethon import tl
from telethon.tl.types import ChatInviteAlready, ChatInvite, Channel
from telethon.tl.functions.messages import CheckChatInviteRequest
from telethon.errors import InviteHashExpiredError

from loaders.channels import BaseChannelsLoader


logger = logging.getLogger(__name__)


class ChannelsManager:
    def __init__(self, client, channels_loader_adaptor: BaseChannelsLoader):
        self.channels_loader_adaptor = channels_loader_adaptor
        self.client = client

    async def get_channels(self) -> List[Channel]:
        return await self._get_channels_objects(self.channels_loader_adaptor)

    async def _get_channels_objects(self, channels_loader: BaseChannelsLoader) -> List[Channel]:
        channels_list = list()

        for channel_info in channels_loader.get_all():
            channel = await self.get_channel(channel_info)

            if channel:
                channels_list.append(channel)
            else:
                logger.error(f"Cant find channel by {channel_info.id}")

        return channels_list

    async def get_channel(self, channel_info):
        channels_from_search = await self.client(functions.contacts.SearchRequest(channel_info.id, limit=5))

        if channel := await self.get_chat_obj(channel_info.id):
            return channel

        try:
            # Try get channel invite object by hash_id
            channel_invite = await self.client(CheckChatInviteRequest(channel_info.id))
            if channel_invite:
                if isinstance(channel_invite, ChatInvite):
                    # If channel_invite is not expired we can try join to the channel
                    channel_updates = await self.client(functions.messages.ImportChatInviteRequest(channel_info.id))
                    channel = channel_updates.chats[0]
                elif isinstance(channel_invite, ChatInviteAlready):
                    # Account already subscribe to the channel and we can just get channel object from channel_invite
                    channel = channel_invite.chat
                if channel:
                    channel = await self.get_chat_obj(channel.id)
                return channel
        except InviteHashExpiredError:
            pass

        # If invite hash expired than we can try just join to channels by request
        try:
            channels_updates = await self.client(functions.channels.JoinChannelRequest(
                channel=channel_info.id
            ))
            return channels_updates.chats[0]
        except ValueError as err:
            pass
        return channels_from_search.chats[0] if channels_from_search else None

    async def get_chat_obj(self, channel_id) -> tl.types.channels.ChannelParticipant or None:
        try:
            channel_obj = await self.client(functions.channels.GetChannelsRequest(
                id=[channel_id]
            ))
        except Exception as e:
            logger.info(e)
            return
        return channel_obj.chats[0]
