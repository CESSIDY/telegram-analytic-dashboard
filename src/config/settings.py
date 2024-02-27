import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB configuration
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
MONGODB_HOST = os.getenv("MONGODB_HOST", "")
MONGODB_PORT = os.getenv("MONGODB_PORT", "")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "")

MONGODB_URI = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}"

# Dash app configuration
DASH_SECRET_KEY = os.getenv("DASH_SECRET_KEY", "your_secret_key")

