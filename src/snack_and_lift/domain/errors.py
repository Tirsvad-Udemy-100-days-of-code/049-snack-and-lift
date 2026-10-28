"""@file errors.py
@brief The errors of the bot.
"""


class GymError(Exception):
    """@brief The gym site did not behave as the bot expected (a page, element or timeout)."""


class LoginFailedError(GymError):
    """@brief The site refused the login; the message is the text the site shows."""


class MissingCredentialsError(Exception):
    """@brief The account e-mail or password is not set in the environment."""
