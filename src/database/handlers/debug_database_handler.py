import logging
import json

from database import BaseDatabaseHandler

logger = logging.getLogger(__name__)


class DebugDatabaseHandler(BaseDatabaseHandler):

    def store_channel(self, channel_id, chat_name, content):
        logger.info(f"channel_id: {channel_id} => chat_name: {chat_name} => content: {json.loads(content)}")

    def store_message(self, channel_id, message_id, content):
        logger.info(f"channel_id: {channel_id} => message_id: {message_id} => content: {json.loads(content)}")

    def store_comment(self, channel_id, message_id, comment_id, content):
        logger.info(f"channel_id: {channel_id} => message_id: {message_id} => comment_id: {comment_id} => "
                    f"content: {json.loads(content)}")

    def get_all_channels(self):
        return []

    def get_messages_by_channel_id(self, channel_id):
        return []

    def get_comments_by_message_id(self, message_id):
        return []

    def get_comments_by_channel_id(self, channel_id):
        return []
