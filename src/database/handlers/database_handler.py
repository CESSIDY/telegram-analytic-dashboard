from datetime import datetime
import logging

from database import BaseDatabaseHandler
from database.models import Message, Comment, Channel
from database.db_connector import connect_to_database


logger = logging.getLogger(__name__)


class DatabaseHandler(BaseDatabaseHandler):

    def __init__(self):
        connect_to_database()
        self.message_index = 1

    def store_channel(self, channel_id, chat_name, content):
        existing_channel = Channel.objects(chat_id=channel_id).first()

        if not existing_channel:
            channel = Channel(chat_id=channel_id, name=chat_name, content=content, timestamp=datetime.now())
            channel.save()
            logger.debug(f"Channel ({channel_id}) stored in the database.")
        else:
            existing_channel.timestamp = datetime.now()
            existing_channel.content = content
            existing_channel.save()
            logger.debug(f"Channel ({channel_id}) already exists.")

    def store_message(self, channel_id, message_id, content):
        # TODO FIX
        existing_message = Message.objects(chat_id=channel_id, message_id=message_id).first()

        if not existing_message:
            message = Message(chat_id=channel_id, message_id=message_id, content=content, timestamp=datetime.now())
            message.save()
            logger.debug(f"Message (chat_id={channel_id}, message_id={message_id}) stored in the database.")
        else:
            existing_message.timestamp = datetime.now()
            existing_message.content = content
            existing_message.save()
            logger.debug(f"Message (chat_id={channel_id}, message_id={message_id}) already exists.")
        self.message_index += 1

    def store_comment(self, channel_id, message_id, comment_id, content):
        existing_comment = Comment.objects(chat_id=channel_id, comment_id=comment_id).first()

        if not existing_comment:
            comment = Comment(chat_id=channel_id, message_id=message_id, comment_id=comment_id,
                              content=content, timestamp=datetime.now())
            comment.save()
            logger.debug(f"Comment (chat_id={channel_id}, message_id={message_id}) stored in the database.")
        else:
            existing_comment.timestamp = datetime.now()
            existing_comment.content = content
            existing_comment.save()
            logger.debug(f"Comment (chat_id={channel_id}, message_id={message_id}) already exists.")

    def get_all_channels(self):
        channels = Channel.objects().all()
        return channels

    def get_messages_by_channel_id(self, channel_id):
        messages = Message.objects(chat_id=channel_id).all()
        return messages

    def get_comments_by_message_id(self, message_id, channel_id):
        comments = Comment.objects(chat_id=channel_id, message_id=message_id).all()
        return comments

    def get_comments_by_channel_id(self, channel_id):
        comments = Comment.objects(chat_id=channel_id).all()
        return comments
