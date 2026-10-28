"""@file test_constants.py
@brief Smoke test: the assignment's values are the ones in constants.py.
"""

from snack_and_lift import constants


def test_gym_address_is_https() -> None:
    assert constants.GYM_URL.startswith("https://")


def test_credentials_are_read_from_named_environment_variables() -> None:
    assert constants.ACCOUNT_EMAIL_ENV == "SNACK_AND_LIFT_EMAIL"
    assert constants.ACCOUNT_PASSWORD_ENV == "SNACK_AND_LIFT_PASSWORD"


def test_login_element_ids() -> None:
    assert constants.NAV_LOGIN_BUTTON_ID == "login-button"
    assert constants.LOGIN_EMAIL_INPUT_ID == "email-input"
    assert constants.LOGIN_PASSWORD_INPUT_ID == "password-input"
    assert constants.LOGIN_SUBMIT_BUTTON_ID == "submit-button"
    assert constants.ERROR_MESSAGE_ID == "error-message"
    assert constants.SCHEDULE_PAGE_ID == "schedule-page"


def test_retry_count_is_seven() -> None:
    assert constants.RETRY_COUNT == 7


def test_bot_books_tuesday_and_thursday() -> None:
    assert constants.TARGET_WEEKDAYS == ("Tue", "Thu")
