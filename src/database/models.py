from datetime import datetime
import json

from mongoengine import Document, StringField, DateTimeField


class Message(Document):
    chat_id = StringField(required=True)
    message_id = StringField(required=True, unique=True)
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.now, required=True)

    # def set_content(self, content):
    #     self.content = json.dumps(content)
    #
    # def get_content(self):
    #     return json.loads(self.content)


class Comment(Document):
    chat_id = StringField(required=True)
    message_id = StringField(required=True)
    comment_id = StringField(required=True, unique=True)
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.now, required=True)

    # def set_content(self, content):
    #     self.content = json.dumps(content)
    #
    # def get_content(self):
    #     return json.loads(self.content)
