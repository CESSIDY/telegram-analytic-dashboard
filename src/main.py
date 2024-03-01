import logging

from utils import configure_logging
from scraper import MessagesScraper
from database import DatabaseHandler, DebugDatabaseHandler
from loaders.channels import JsonChannelsLoader
from loaders.accounts import JsonAccountsLoader

configure_logging()
logger = logging.getLogger(__name__)


def main():
    db_handler = DatabaseHandler()
    scraper = MessagesScraper(JsonChannelsLoader(), JsonAccountsLoader(), db_handler)
    scraper.run_scraper()
    # # Connect to the database
    #
    # # Initialize the web app
    # app = create_app(db_handler)
    #
    # # Define routes and callbacks (if any)
    # # app.callback(...)
    # # app.layout = ...
    #
    # if __name__ == '__main__':
    #     app.run_server(debug=True)


if __name__ == "__main__":
    main()
