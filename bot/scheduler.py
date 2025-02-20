from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import get_db_connection
from config import logger

scheduler = AsyncIOScheduler()


def start_scheduler():
    """Запускает планировщик."""
    scheduler.start()


async def send_scheduled_message(app):
    """Отправляет запланированные сообщения."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, chat_id, message FROM scheduled_messages WHERE send_time <= NOW() AND sent = FALSE")
        messages = cur.fetchall()
        for msg_id, chat_id, message in messages:
            if not message.strip():
                logger.error(f"Ошибка: пустое сообщение (id={msg_id})")
                continue
            try:
                await app.bot.send_message(chat_id=chat_id, text=message)
                cur.execute("UPDATE scheduled_messages SET sent = TRUE WHERE id = %s", (msg_id,))
                logger.info(f"Запуск задачи {job_id} на {send_time}")
            except Exception as e:
                logger.error(f"Ошибка отправки сообщения {msg_id}: {e}")
        conn.commit()
        cur.close()
    except Exception as e:
        logger.error(f"Ошибка работы с базой: {e}")
    finally:
        conn.close()
