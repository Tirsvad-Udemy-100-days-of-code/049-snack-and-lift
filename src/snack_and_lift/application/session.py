"""@file session.py
@brief Lecture step 2: the login of the bot.
"""

import logging

from snack_and_lift.application.credentials import Credentials
from snack_and_lift.application.ports import GymPort

logger = logging.getLogger(__name__)


def login(gym: GymPort, credentials: Credentials) -> None:
    """@brief Log in and wait until the class schedule is shown.

    @param gym The gym site.
    @param credentials The account to log in with.
    @exception LoginFailedError The login failed; `retry` repeats it (lecture step 9).
    """
    gym.log_in(credentials.email, credentials.password)
    logger.info("✓ Logged in: the class schedule is shown")
