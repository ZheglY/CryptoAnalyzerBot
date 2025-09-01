import os
from dotenv import load_dotenv, find_dotenv
from utils.logger import get_logger


logger = get_logger(__name__)

if not find_dotenv():
    logger.critical('Environment variables are not loaded because the .env file is missing')
    exit(1)
else:
    load_dotenv()
    logger.debug('env file variables loaded')


BOT_TOKEN = os.getenv('BOT_TOKEN')