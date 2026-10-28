"""@file verification.py
@brief Lecture steps 7 and 8: check the bookings on the My Bookings page.
"""

import logging
import time
from collections.abc import Sequence

from snack_and_lift import constants
from snack_and_lift.application.ports import GymPort
from snack_and_lift.application.retry import Sleep, retry
from snack_and_lift.domain.booking_entry import BookingEntry, is_target_entry
from snack_and_lift.domain.errors import NoBookingsFoundError
from snack_and_lift.domain.models import ClassResult
from snack_and_lift.domain.verification import VerificationResult, build_verification

logger = logging.getLogger(__name__)


def get_my_bookings(gym: GymPort) -> list[BookingEntry]:
    """@brief Open the My Bookings page and read all its entries.

    @param gym The gym site.
    @return Every confirmed booking and waitlist entry, not only the target classes.
    @exception NoBookingsFoundError The page shows no entry at all.
    @exception GymError The page could not be opened or read.
    """
    gym.open_my_bookings()
    entries = gym.list_my_bookings()
    if not entries:
        raise NoBookingsFoundError(constants.MESSAGE_NO_BOOKINGS_FOUND)
    return entries


def get_my_bookings_with_retry(
    gym: GymPort, retries: int = constants.RETRY_COUNT, sleep: Sleep = time.sleep
) -> list[BookingEntry]:
    """@brief Read the My Bookings page, repeating it when the page fails to load.

    @param gym The gym site.
    @param retries The most attempts to make.
    @param sleep Waits between two attempts.
    @return Every confirmed booking and waitlist entry.
    @exception RetriesExhaustedError Every attempt failed.
    """
    return retry(
        lambda: get_my_bookings(gym), retries, constants.RETRY_DESCRIPTION_BOOKINGS, sleep=sleep
    )


def verify_bookings(
    gym: GymPort,
    results: Sequence[ClassResult],
    retries: int = constants.RETRY_COUNT,
    sleep: Sleep = time.sleep,
) -> VerificationResult:
    """@brief Compare what the bot booked with the My Bookings page.

    The page is not opened when the bot handled no class.

    @param gym The gym site.
    @param results What happened to each class.
    @param retries The most attempts to read the page.
    @param sleep Waits between two attempts.
    @return The comparison of the expected entries with the Tuesday and Thursday 6pm entries.
    @exception RetriesExhaustedError The page could not be read on any attempt.
    """
    if not results:
        return build_verification(results, [])
    entries = [
        entry for entry in get_my_bookings_with_retry(gym, retries, sleep) if is_target_entry(entry)
    ]
    return build_verification(results, entries)
