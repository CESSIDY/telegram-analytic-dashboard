from datetime import datetime
import json
from typing import List, Dict

from mongoengine import Document, StringField, DateTimeField, IntField


class Channel(Document):
    chat_id = IntField(required=True)
    name = StringField(required=True)
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.now, required=True)

    # def set_content(self, content):
    #     self.content = json.dumps(content)
    #
    def get_content(self):
        return json.loads(self.content)

    def to_dict_for_analysis(self) -> Dict:
        channel_dict = {"id": self.chat_id,
                        "name": self.name}
        return channel_dict


class BaseMessage:
    chat_id = IntField(required=True)
    message_id = IntField(required=True)
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.now, required=True)

    def get_content(self) -> Dict:
        return json.loads(self.content)

    def get_content_datetime(self):
        timezone_offset = -6
        content = self.get_content()
        return datetime.fromisoformat(content.get('date')[:timezone_offset])

    def get_emojis_reactions(self):
        content = self.get_content()
        reactions = []
        if content.get('reactions'):
            reactions = content.get('reactions').get('results')
        emojis = {}
        for reaction in reactions:
            count = reaction.get('count')
            emoticon = []
            if reaction.get('reaction'):
                emoticon = reaction.get('reaction').get('emoticon')
            if emoticon and count:
                emojis[emoticon] = count
        return emojis


class Message(BaseMessage, Document):
    # chat = ReferenceField(Channel)
    def to_dict_for_analysis(self) -> Dict:
        content = self.get_content()
        emojis = self.get_emojis_reactions()
        main_emoji_reaction = max(emojis, key=emojis.get) if emojis else None

        last_update_datetime = self.get_content_datetime()
        last_update_date = last_update_datetime.date()
        last_update_date_month = last_update_datetime.strftime("%B")
        message_dict = {
            "id": self.message_id,
            "channel_id": self.chat_id,
            "datetime": last_update_datetime,
            "date": last_update_date,
            "month": last_update_date_month,
            "message": content.get('message'),
            "views": int(content.get('views', 0)),
            "forwards": int(content.get('forwards', 0)),
            "reactions": sum(emojis.values()),
            "emojis": emojis,
            "main_emoji_reaction": main_emoji_reaction,
        }
        return message_dict


class Comment(BaseMessage, Document):
    # chat = ReferenceField(Channel)
    # message = ReferenceField(Message)
    comment_id = IntField(required=True, unique=True)

    def to_dict_for_analysis(self) -> Dict:
        content = self.get_content()

        user_id = content.get('from_id', {}).get('user_id')
        emojis = self.get_emojis_reactions()

        last_update_datetime = self.get_content_datetime()
        last_update_date = last_update_datetime.date()
        last_update_date_month = last_update_datetime.strftime("%B")

        comment_dict = {
            "id": self.comment_id,
            "message_id": self.message_id,
            "channel_id": self.chat_id,
            "datetime": last_update_datetime,
            "date": last_update_date,
            "month": last_update_date_month,
            "message": content.get('message'),
            "user_id": user_id,
            "reactions": sum(emojis.values()),
            "emojis": emojis,
        }

        return comment_dict
