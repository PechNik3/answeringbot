import unittest
from unittest.mock import patch, MagicMock
from bot.scheduler import send_scheduled_message
from bot.database import get_db_connection


class TestScheduler(unittest.TestCase):

    @patch("bot.database.get_db_connection")
    @patch("bot.scheduler.scheduler.add_job")
    async def test_send_scheduled_message(self, mock_add_job, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Мокируем выборку запланированных сообщений
        mock_cursor.fetchall.return_value = [(1, 12345, "Test message")]

        app = MagicMock()
        await send_scheduled_message(app)

        mock_cursor.execute.assert_called_with(
            "SELECT id, chat_id, message FROM scheduled_messages WHERE send_time <= NOW() AND sent = FALSE"
        )
        app.bot.send_message.assert_called_with(chat_id=12345, text="Test message")


if __name__ == "__main__":
    unittest.main()
