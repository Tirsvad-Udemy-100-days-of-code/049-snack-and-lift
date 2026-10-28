"""@file errors.py
@brief The errors of the bot.
"""


class GymError(Exception):
    """@brief The gym site did not behave as the bot expected (a page, element or timeout)."""


class LoginFailedError(GymError):
    """@brief The site refused the login; the message is the text the site shows."""


class MissingCredentialsError(Exception):
    """@brief The account e-mail or password is not set in the environment."""


class UnknownButtonError(GymError):
    """@brief A class button shows a text the bot cannot act on (busy, completed or unknown)."""


class PageFormatError(GymError):
    """@brief A text read from the page (a day label or a time) has an unexpected format."""


class NoBookingsFoundError(GymError):
    """@brief The My Bookings page shows no booking where the bot expects some.

    The project's counterpart of Selenium's `NoSuchElementException`, which the lecture asks
    the student to raise when the bookings that should be there are missing.
    """
