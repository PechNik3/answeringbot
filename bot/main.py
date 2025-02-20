import asyncio
import nest_asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN
from handlers import start, handle_message, schedule_message
from scheduler import start_scheduler


async def main():
    """Главная асинхронная функция запуска бота."""
    start_scheduler()

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("schedule", schedule_message))

    await application.run_polling()


if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
