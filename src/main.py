from utils import configure_logging
from web_app.app import *

configure_logging()


if __name__ == "__main__":
    print("Starting server...")
    run_server()
