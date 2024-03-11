import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    # MongoDB configuration
    MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
    MONGODB_HOST = os.getenv("MONGODB_HOST", "")
    MONGODB_PORT = int(os.getenv("MONGODB_PORT", ""))
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "")

    MONGODB_URI = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}"

    # Dash app configuration
    DASH_SECRET_KEY = os.getenv("DASH_SECRET_KEY", "your_secret_key")
    DASH_PORT = int(os.getenv("PYTHON_PORT", "8051"))
    DASH_DEBUG = bool(int(os.getenv("DASH_DEBUG", 0)))

    # Redis configuration
    REDIS_ADDRESS = os.getenv("REDIS_ADDRESS", "redis")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    REDIS_URL = f"redis://{REDIS_ADDRESS}:{REDIS_PORT}/0"

    # Proxy configuration
    PROXY_ENABLED = int(os.getenv("PROXY_ENABLED", 0))
    PROXY_USERNAME = os.getenv("PROXY_USERNAME", "")
    PROXY_PASSWORD = os.getenv("PROXY_PASSWORD", "")
    PROXY_ADDRESS = os.getenv("PROXY_ADDRESS", "")
    PROXY_PORT = os.getenv("PROXY_PORT", "")
    PROXY_TYPE = os.getenv("PROXY_TYPE", "")

    # Telegram configuration
    TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID", "")
    TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")
    TELEGRAM_USERNAME = os.getenv("TELEGRAM_USERNAME", "")
    TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE", "")


settings = Settings()
