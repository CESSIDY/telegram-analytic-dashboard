from . import BaseChannelsLoader
from models import ChannelLoaderModel
from typing import List


class ListChannelsLoader(BaseChannelsLoader):

    def __init__(self):
        super(ListChannelsLoader, self).__init__()

    def _parse_all_comments(self) -> List[ChannelLoaderModel]:
        return [ChannelLoaderModel(id="bwt_commentator_test_1", private=False),
                ChannelLoaderModel(id="If7N8EnSEWViYzgy", private=True)]
