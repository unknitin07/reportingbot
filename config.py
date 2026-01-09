import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000')
SUPER_ADMIN_ID = int(os.getenv('SUPER_ADMIN_ID', '5813016547'))

# Database Configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', 'bot_database.db')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = 'bot.log'

# Bot Settings
COMMAND_COOLDOWN = 2  # seconds
API_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
TASK_REFRESH_INTERVAL = 30  # seconds

# Conversation States
(PHONE, CODE, PASSWORD, 
 SELECT_ACCOUNTS, TARGET, MESSAGE, CONFIRM,
 ACCOUNTS, TITLE, DESCRIPTION, PUBLIC,
 TARGETS, REASON, INTERVAL) = range(13)

# User Status
STATUS_PENDING = 'pending'
STATUS_APPROVED = 'approved'
STATUS_BLOCKED = 'blocked'
