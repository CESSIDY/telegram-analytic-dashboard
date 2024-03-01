from datetime import datetime
import json

from mongoengine import Document, StringField, DateTimeField, IntField


class Channel(Document):
    chat_id = IntField(required=True)
    name = StringField(required=True)
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.now, required=True)

    # def set_content(self, content):
    #     self.content = json.dumps(content)
    #
    # def get_content(self):
    #     return json.loads(self.content)


class Message(Document):
    # chat = ReferenceField(Channel)
    chat_id = IntField(required=True)
    message_id = IntField(required=True, unique=True)
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.now, required=True)

    # def set_content(self, content):
    #     self.content = json.dumps(content)
    #
    # def get_content(self):
    #     return json.loads(self.content)


class Comment(Document):
    # chat = ReferenceField(Channel)
    # message = ReferenceField(Message)
    chat_id = IntField(required=True)
    message_id = IntField(required=True)
    comment_id = IntField(required=True, unique=True)
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.now, required=True)

    # def set_content(self, content):
    #     self.content = json.dumps(content)
    #
    # def get_content(self):
    #     return json.loads(self.content)
