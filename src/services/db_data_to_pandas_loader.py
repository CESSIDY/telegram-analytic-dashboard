from typing import List, Dict

import pandas as pd

from database import BaseDatabaseHandler


class DBDataToPandasLoader:
    def __init__(self, database_handler: BaseDatabaseHandler):
        self.database_handler = database_handler

    def get_channels(self) -> pd.DataFrame:
        channels_from_db = self.database_handler.get_all_channels()
        channels_list = []
        for channel in channels_from_db:
            channels_list.append(channel.to_dict_for_analysis())
        return self._to_dataframe(channels_list)

    def get_messages_df_by_channel_id(self, channel_id) -> pd.DataFrame:
        messages_from_db = self.database_handler.get_messages_by_channel_id(channel_id)
        if not messages_from_db:
            return pd.DataFrame([])
        messages_list = []
        for message in messages_from_db:
            message_dict = message.to_dict_for_analysis()
            if not message_dict['message']:
                continue
            messages_list.append(message_dict)
        return self._to_dataframe(messages_list).sort_values(by=['date']).reset_index()

    def get_comments_df_by_channel_id(self, channel_id) -> pd.DataFrame:
        comments_from_db = self.database_handler.get_comments_by_channel_id(channel_id)
        if not comments_from_db:
            return pd.DataFrame([])
        comments_list = []
        for comment in comments_from_db:
            comments_list.append(comment.to_dict_for_analysis())
        return self._to_dataframe(comments_list).sort_values(by=['date']).reset_index()

    def get_comments_df_by_message_id(self, message_id) -> pd.DataFrame:
        comments_from_db = self.database_handler.get_comments_by_message_id(message_id)
        if not comments_from_db:
            return pd.DataFrame([])
        comments_list = []
        for comment in comments_from_db:
            comments_list.append(comment.to_dict_for_analysis())
        return self._to_dataframe(comments_list).sort_values(by=['date']).reset_index()

    def get_all_emojis_reactions_in_channel(self, channel_id):
        messages_from_db = self.database_handler.get_messages_by_channel_id(channel_id)
        uniq_emojis = set()
        for message in messages_from_db:
            message_dict = message.to_dict_for_analysis()
            emojis = message_dict['emojis']
            if not emojis:
                continue
            for emoji in emojis.keys():
                uniq_emojis.add(emoji)
        return uniq_emojis

    @staticmethod
    def _to_dataframe(data: List[Dict]) -> pd.DataFrame:
        df_data = pd.DataFrame(data=data)
        return df_data
