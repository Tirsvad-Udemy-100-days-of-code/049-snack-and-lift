"""@file console_recorder.py
@brief Keeps the lines the bot logs, so they can be drawn as the lecture's console screenshot.
"""

import logging


class ConsoleRecorder(logging.Handler):
    """@brief A logging handler that stores the formatted message of every record."""

    def __init__(self, level: int = logging.NOTSET) -> None:
        """@brief Create an empty recorder.

        @param level The lowest level to keep.
        """
        super().__init__(level)
        self.setFormatter(logging.Formatter("%(message)s"))
        self._lines: list[str] = []

    @property
    def lines(self) -> list[str]:
        """@brief The recorded lines, oldest first (a copy)."""
        return list(self._lines)

    @property
    def text(self) -> str:
        """@brief The recorded lines joined by newlines."""
        return "\n".join(self._lines)

    def emit(self, record: logging.LogRecord) -> None:
        """@brief Store one record.

        @param record The log record.
        """
        self._lines.append(self.format(record))
