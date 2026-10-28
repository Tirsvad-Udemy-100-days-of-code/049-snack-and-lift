"""@file session.py
@brief Lecture step 2: the login of the bot.
"""

import logging
import time

from snack_and_lift import constants
from snack_and_lift.application.credentials import Credentials
from snack_and_lift.application.ports import GymPort
from snack_and_lift.application.retry import Sleep, retry

logger = logging.getLogger(__name__)


def login(gym: GymPort, credentials: Credentials) -> None:
    """@brief Log in and wait until the class schedule is shown.

    @param gym The gym site.
    @param credentials The account to log in with.
    @exception LoginFailedError The login failed; `retry` repeats it (lecture step 9).
    """
    gym.log_in(credentials.email, credentials.password)
    logger.info("✓ Logged in: the class schedule is shown")


def login_with_retry(
    gym: GymPort,
    credentials: Credentials,
    retries: int = constants.RETRY_COUNT,
    sleep: Sleep = time.sleep,
) -> None:
    """@brief Log in, repeating the login when the site drops the request.

    @param gym The gym site.
    @param credentials The account to log in with.
    @param retries The most attempts to make.
    @param sleep Waits between two attempts.
    @exception RetriesExhaustedError Every attempt failed.
    """
    retry(
        lambda: login(gym, credentials),
        retries,
        constants.RETRY_DESCRIPTION_LOGIN,
        sleep=sleep,
    )
