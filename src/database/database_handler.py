from datetime import datetime

from database import BaseDatabaseHandler
from database.models import Message, Comment, Channel


class DatabaseHandler(BaseDatabaseHandler):

    def store_channel(self, chat_id, chat_name, content):
        existing_channel = Channel.objects(chat_id=chat_id).first()

        if not existing_channel:
            channel = Channel(chat_id=chat_id, chat_name=chat_name, content=content, timestamp=datetime.now())
            channel.save()
            print("Channel stored in the database.")
        else:
            existing_channel.timestamp = datetime.now()
            existing_channel.content = content
            existing_channel.save()
            print("Channel already exists. Updated content and timestamp.")

    def store_message(self, chat_id, message_id, content):
        existing_message = Message.objects(message_id=message_id).first()

        if not existing_message:
            message = Message(chat_id=chat_id, message_id=message_id, content=content, timestamp=datetime.now())
            message.save()
            print("Message stored in the database.")
        else:
            existing_message.timestamp = datetime.now()
            existing_message.content = content
            existing_message.save()
            print("Message already exists. Updated content and timestamp.")

    def store_comment(self, chat_id, message_id, comment_id, content):
        existing_comment = Comment.objects(comment_id=comment_id).first()

        if not existing_comment:
            comment = Comment(chat_id=chat_id, message_id=message_id, comment_id=comment_id,
                              content=content, timestamp=datetime.now())
            comment.save()
            print("Comment stored in the database.")
        else:
            existing_comment.timestamp = datetime.now()
            existing_comment.content = content
            existing_comment.save()
            print("Comment already exists. Updated content and timestamp.")

    def get_messages_by_chat_id(self, chat_id):
        messages = Message.objects(chat_id=chat_id).all()
        return messages

    def get_comments_by_message_id(self, message_id):
        comments = Comment.objects(message_id=message_id).all()
        return comments

    def get_comments_by_chat_id(self, chat_id):
        comments = Comment.objects(chat_id=chat_id).all()
        return comments
