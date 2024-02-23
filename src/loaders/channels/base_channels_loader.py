from abc import ABC, abstractmethod
from typing import List
from models import ChannelLoaderModel


class BaseChannelsLoader(ABC):
    _channels_models_list: List[ChannelLoaderModel]

    def __init__(self):
        self._channels_models_list = self._parse_all_comments()

    def get_all(self) -> List[ChannelLoaderModel]:
        return self._channels_models_list

    @abstractmethod
    def _parse_all_comments(self) -> List[ChannelLoaderModel]:
        pass
