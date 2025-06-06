import os
from dotenv import load_dotenv
load_dotenv()

# Openrouter configuration
OPENROUTER_KEY = os.getenv('OPENROUTER_KEY')
if not OPENROUTER_KEY:
    raise ValueError("OPENROUTER_KEY environment variable is not set")

# PostgreSQL configuration
DB_URL = os.getenv('DB_URL')
if not DB_URL:
    raise ValueError("DB_URL environment variable is not set")

# Admins info
ADMINS_CHAT_ID = os.getenv('ADMINS_CHAT_ID')
if not ADMINS_CHAT_ID:
    raise ValueError("ADMINS_CHAT_ID environment variable is not set")

# Exports info
DELETE_EXPORTS = os.getenv('DELETE_EXPORTS', True)

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")
