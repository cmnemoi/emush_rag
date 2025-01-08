from datetime import datetime, timedelta


class FakeDateTime:
    """A fake datetime for testing that allows controlling the current time"""

    def __init__(self, initial_time: datetime = datetime(2024, 1, 1)):
        self._current_time = initial_time

    def now(self) -> datetime:
        return self._current_time

    def advance(self, seconds: int) -> None:
        """Advance the current time by the specified number of seconds"""
        self._current_time += timedelta(seconds=seconds)
