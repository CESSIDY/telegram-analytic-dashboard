import logging
import os
from telethon.sync import TelegramClient
from loaders.accounts import JsonAccountsLoader
from loaders.channels import JsonChannelsLoader
from models import AccountsLoaderModel
from utils import session_files_path, get_proxy_configurations, configure_logging
from workers import ChannelsScraper

configure_logging()
logger = logging.getLogger(__name__)


def main():
    accounts_loader = JsonAccountsLoader()
    account_models = accounts_loader.get_all()

    account_models = init_sessions(account_models)
    run_channels_scraper_for_each_account(account_models)


def init_sessions(account_models: [AccountsLoaderModel]) -> [AccountsLoaderModel]:
    correct_account_models = list()

    for account in account_models:
        print(f"Login for: {account.username}")
        try:
            client = run_and_return_client(account)
            client.disconnect()
            correct_account_models.append(account)
        except Exception as err:
            print(f"Authorization error for {account.username}")
            logger.error(err)

    return correct_account_models


def run_and_return_client(account_model: AccountsLoaderModel):
    session_path = os.path.join(session_files_path, account_model.username)

    proxy = get_proxy_configurations()
    if proxy:
        client = TelegramClient(session_path, account_model.api_id, account_model.api_hash, proxy=proxy)
    else:
        client = TelegramClient(session_path, account_model.api_id, account_model.api_hash)

    client.start()
    return client


def run_channels_scraper_for_each_account(account_models: [AccountsLoaderModel]):
    channels_loader = JsonChannelsLoader()
    scraper_adapter = None  # TODO
    storage_adapter = None  # TODO

    for account_model in account_models:
        print(f"Start processing for {account_model.username}")
        client = run_and_return_client(account_model)

        scraper = ChannelsScraper(client, channels_loader, scraper_adapter, storage_adapter)
        scraper.run_until_complete()

        client.disconnect()
        print(f"Finish processing for {account_model.username}")


if __name__ == "__main__":
    main()
