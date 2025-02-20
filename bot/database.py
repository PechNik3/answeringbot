import psycopg2
from config import DB_CONFIG, logger


def get_db_connection():
    """Устанавливает соединение с базой данных и создает таблицы, если их нет."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        create_tables_if_not_exists(conn)
        return conn
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        return None


def create_tables_if_not_exists(conn):
    """Создает таблицы, если их нет в базе данных."""
    try:
        cur = conn.cursor()

        # Создание таблицы scheduled_messages
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scheduled_messages (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT NOT NULL,
                message TEXT NOT NULL,
                send_time TIMESTAMP NOT NULL,
                sent BOOLEAN DEFAULT FALSE
            )
        """)

        # Создание таблицы messages
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cur.close()
    except Exception as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
