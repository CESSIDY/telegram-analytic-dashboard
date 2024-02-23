from typing import List
from models import AccountsLoaderModel
from .base_accounts_loader import BaseAccountsLoader
import os
import json
import logging

logger = logging.getLogger(__name__)


class JsonAccountsLoader(BaseAccountsLoader):
    def __init__(self):
        self.base_accounts_path = os.path.abspath(os.path.join(os.path.realpath(__file__),
                                                               "..", "..", "..", "..", "data", "accounts"))
        super(JsonAccountsLoader, self).__init__()

    def _parse_all_accounts(self) -> List[AccountsLoaderModel]:
        json_files = self._get_all_json_accounts_files()
        accounts_list = self._get_accounts_from_json_files(json_files)
        account_models_list = self._convert_accounts_list_to_account_models(accounts_list)

        logger.info(f"accounts: {len(account_models_list)}")
        return account_models_list

    def _get_all_json_accounts_files(self) -> list:
        json_files = []
        for pos_json in os.listdir(self.base_accounts_path):
            if pos_json.endswith('.json'):
                json_files.append(os.path.join(self.base_accounts_path, pos_json))

        return json_files

    @staticmethod
    def _get_accounts_from_json_files(json_files: list) -> List[dict]:
        accounts_list = []
        for json_file in json_files:
            with open(json_file, "r") as file:
                json_accounts = file.read()
                accounts = json.loads(json_accounts)
                accounts_list.extend(accounts)
        return accounts_list

    @staticmethod
    def _convert_accounts_list_to_account_models(accounts_list: List[dict]) -> List[AccountsLoaderModel]:
        accounts_models_list = []

        for account in accounts_list:
            if account.get("api_id") and account.get("api_hash") and account.get("username") \
                    and isinstance(account.get("api_id"), int):
                account_model = AccountsLoaderModel(api_id=account["api_id"],
                                                    api_hash=account["api_hash"],
                                                    username=account["username"],
                                                    )
                accounts_models_list.append(account_model)
            else:
                logger.warning(f"Can't load account obj: {account}. Must be [api_id: int, api_hash: str, username: str]")
        return accounts_models_list
