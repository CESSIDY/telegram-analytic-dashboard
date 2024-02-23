from abc import ABC, abstractmethod
from typing import List
from models import AccountsLoaderModel


class BaseAccountsLoader(ABC):
    _accounts_list: List[AccountsLoaderModel]

    def __init__(self):
        self._accounts_list = self._parse_all_accounts()

    def get_all(self) -> List[AccountsLoaderModel]:
        return self._accounts_list

    @abstractmethod
    def _parse_all_accounts(self):
        pass
