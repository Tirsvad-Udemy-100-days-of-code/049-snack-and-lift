"""@file verification.py
@brief Lecture steps 7 and 8: check the bookings on the My Bookings page.
"""

import logging
from collections.abc import Sequence

from snack_and_lift import constants
from snack_and_lift.application.ports import GymPort
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


def verify_bookings(gym: GymPort, results: Sequence[ClassResult]) -> VerificationResult:
    """@brief Compare what the bot booked with the My Bookings page.

    The page is not opened when the bot handled no class.

    @param gym The gym site.
    @param results What happened to each class.
    @return The comparison of the expected entries with the Tuesday and Thursday 6pm entries.
    @exception NoBookingsFoundError Classes were handled but the page shows no entry.
    @exception GymError The page could not be opened or read.
    """
    if not results:
        return build_verification(results, [])
    entries = [entry for entry in get_my_bookings(gym) if is_target_entry(entry)]
    return build_verification(results, entries)
