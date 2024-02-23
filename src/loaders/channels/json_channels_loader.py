from . import BaseChannelsLoader
import os
import json
import logging
from typing import List
from models import ChannelLoaderModel

logger = logging.getLogger(__name__)


class JsonChannelsLoader(BaseChannelsLoader):

    def __init__(self):
        self.base_channels_path = os.path.abspath(os.path.join(os.path.realpath(__file__),
                                                               "..", "..", "..", "..", "data", "channels"))
        super(JsonChannelsLoader, self).__init__()

    def _parse_all_comments(self) -> List[ChannelLoaderModel]:
        json_files = self._get_all_json_channels_files()
        channels_list = self._get_channels_from_json_files(json_files)
        channels_models_list = self._convert_channels_list_to_channel_models(channels_list)

        logger.info(f"channels: {len(channels_models_list)}")
        return channels_models_list

    def _get_all_json_channels_files(self) -> list:
        json_files = []
        for pos_json in os.listdir(self.base_channels_path):
            if pos_json.endswith('.json'):
                json_files.append(os.path.join(self.base_channels_path, pos_json))

        return json_files

    @staticmethod
    def _get_channels_from_json_files(json_files: list) -> List[dict]:
        channels_list = []
        for json_file in json_files:
            with open(json_file, "r") as file:
                json_channels = file.read()
                channels = json.loads(json_channels)
                channels_list.extend(channels)
        return channels_list

    @staticmethod
    def _convert_channels_list_to_channel_models(channels_list: List[dict]) -> List[ChannelLoaderModel]:
        channels_models_list = []

        for channel in channels_list:
            if channel.get("id") and isinstance(channel.get("private"), bool):
                channel_model = ChannelLoaderModel(id=channel["id"], private= channel["private"])
                channels_models_list.append(channel_model)
            else:
                logger.warning(f"Can't load channel obj: {channel}")
        return channels_models_list
