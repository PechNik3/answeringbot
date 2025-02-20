from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext
from database import get_db_connection
from scheduler import scheduler, send_scheduled_message


def validate_schedule_args(args):
    """Проверяет корректность аргументов для /schedule."""
    if len(args) < 3:
        return None, "Использование: /schedule YYYY-MM-DD HH:MM сообщение"
    try:
        send_time = datetime.strptime(f"{args[0]} {args[1]}", "%Y-%m-%d %H:%M")
        message = " ".join(args[2:]).strip()
        return (send_time, message), None
    except ValueError:
        return None, "Неверный формат даты. Используйте: YYYY-MM-DD HH:MM сообщение"


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я автоматический бот для обработки сообщений.")


async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    await update.message.reply_text(f"Вы сказали: {user_message}")


async def schedule_message(update: Update, context: CallbackContext):
    validation_result, error = validate_schedule_args(context.args)
    if error:
        await update.message.reply_text(error)
        return

    send_time, message = validation_result
    chat_id = update.message.chat_id
    conn = get_db_connection()
    if not conn:
        await update.message.reply_text("Ошибка подключения к базе данных.")
        return

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO scheduled_messages (chat_id, message, send_time, sent) VALUES (%s, %s, %s, FALSE)",
            (chat_id, message, send_time)
        )
        conn.commit()
        cur.close()

        # Используем уникальный идентификатор для задачи
        job_id = f"{chat_id}_{send_time}"

        # Проверяем, существует ли уже задача с таким job_id
        if scheduler.get_job(job_id):
            await update.message.reply_text("Сообщение уже запланировано на это время.")
            return

        scheduler.add_job(
            send_scheduled_message,
            trigger="date",
            run_date=send_time,
            args=[context.application],
            id=job_id,
            replace_existing=True,
            max_instances = 1,
            misfire_grace_time = 10
        )

        await update.message.reply_text(f"Сообщение запланировано на {send_time}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при сохранении в БД: {e}")
    finally:
        conn.close()
