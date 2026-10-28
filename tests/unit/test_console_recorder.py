"""@file test_console_recorder.py
@brief The recorder keeps the formatted lines of the log.
"""

import logging

from snack_and_lift.infrastructure.console_recorder import ConsoleRecorder


def test_recorder_keeps_formatted_messages() -> None:
    logger = logging.getLogger("test_console_recorder")
    logger.setLevel(logging.INFO)
    recorder = ConsoleRecorder()
    logger.addHandler(recorder)
    try:
        logger.info("✓ Logged %s", "in")
        logger.warning("careful")
    finally:
        logger.removeHandler(recorder)

    assert recorder.lines == ["✓ Logged in", "careful"]
    assert recorder.text == "✓ Logged in\ncareful"


def test_recorder_lines_are_a_copy() -> None:
    recorder = ConsoleRecorder()

    recorder.lines.append("x")

    assert recorder.lines == []
