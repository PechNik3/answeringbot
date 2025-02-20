import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from telegram import Update
from telegram.ext import CallbackContext
from bot.handlers import start, handle_message, schedule_message


class TestBotHandlers(unittest.IsolatedAsyncioTestCase):

    @patch("telegram.Update")
    @patch("telegram.ext.CallbackContext")
    async def test_start_handler(self, mock_context, mock_update):
        mock_update.message.reply_text = AsyncMock()
        await start(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with("Привет! Я автоматический бот для обработки сообщений.")

    @patch("telegram.Update")
    @patch("telegram.ext.CallbackContext")
    async def test_handle_message(self, mock_context, mock_update):
        mock_update.message.text = "Hello"
        mock_update.message.reply_text = AsyncMock()
        await handle_message(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with("Вы сказали: Hello")

    @patch("bot.database.get_db_connection")
    @patch("bot.scheduler.scheduler.add_job")
    @patch("telegram.Update")
    @patch("telegram.ext.CallbackContext")
    async def test_schedule_message(self, mock_context, mock_update, mock_add_job, mock_get_db_connection):
        # Создаем моки для обновлений и контекста
        mock_update.message.chat_id = 12345
        mock_update.message.reply_text = AsyncMock()
        mock_context.args = ["2025-02-20", "14:30", "Test message"]

        # Настройка mock-объектов для соединения с БД
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Вызов функции schedule_message
        await schedule_message(mock_update, mock_context)

        # Проверка, что execute был вызван с правильными параметрами
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO scheduled_messages (chat_id, message, send_time, sent) VALUES (%s, %s, %s, FALSE)",
            (12345, "Test message", "2025-02-20 14:30:00")
        )

        # Проверка, что add_job был вызван
        mock_add_job.assert_called_once()


if __name__ == "__main__":
    unittest.main()
