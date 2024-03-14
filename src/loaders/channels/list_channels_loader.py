from . import BaseChannelsLoader
from loaders.loaders_models import ChannelLoaderModel
from typing import List


class ListChannelsLoader(BaseChannelsLoader):

    def __init__(self):
        super(ListChannelsLoader, self).__init__()

    def _parse_all_comments(self) -> List[ChannelLoaderModel]:
        return [ChannelLoaderModel(id="some_test_chat"),
                ChannelLoaderModel(id="nSd21d12eD54")]
