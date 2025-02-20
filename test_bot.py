from bot.handlers import validate_schedule_args


def test_validate_schedule_args():
    assert validate_schedule_args(["2025-02-20", "12:00", "Hello"]) == ((datetime(2025, 2, 20, 12, 0), "Hello"), None)
    assert validate_schedule_args(["wrong", "format"]) == (None, "Использование: /schedule YYYY-MM-DD HH:MM сообщение")
    assert validate_schedule_args(["2025-02-20", "12:00"]) == (
    None, "Использование: /schedule YYYY-MM-DD HH:MM сообщение")
