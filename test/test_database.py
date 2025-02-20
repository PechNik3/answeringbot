import unittest
from unittest.mock import patch, MagicMock
from bot.database import get_db_connection


class TestDatabaseConnection(unittest.TestCase):

    @patch("psycopg2.connect")
    def test_get_db_connection_success(self, mock_connect):
        mock_connect.return_value = MagicMock()
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        mock_connect.assert_called_once_with(
            dbname="answering_bot_db",
            user="postgres",
            password="rootroot",
            host="localhost"
        )

    @patch("psycopg2.connect")
    def test_get_db_connection_failure(self, mock_connect):
        mock_connect.side_effect = Exception("Connection error")
        conn = get_db_connection()
        self.assertIsNone(conn)


if __name__ == "__main__":
    unittest.main()
