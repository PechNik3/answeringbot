import logging

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "BOT_TOKEN"
DB_CONFIG = {
    "dbname": "answering_bot_db",
    "user": "postgres",
    "password": "rootroot",
    "host": "db"
}
