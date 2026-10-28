"""@file test_constants.py
@brief Smoke test: the assignment's values are the ones in constants.py.
"""

from snack_and_lift import constants


def test_gym_address_is_https() -> None:
    assert constants.GYM_URL.startswith("https://")


def test_retry_count_is_seven() -> None:
    assert constants.RETRY_COUNT == 7


def test_bot_books_tuesday_and_thursday() -> None:
    assert constants.TARGET_WEEKDAYS == ("Tue", "Thu")
