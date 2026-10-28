"""@file test_application_verification.py
@brief Reading the My Bookings page and verifying the bookings, against a fake gym.
"""

import pytest
from tests.unit.fakes import FakeGym, no_sleep
from tests.unit.test_booking_entry import make_entry
from tests.unit.test_models import make_card

from snack_and_lift.application.booking import book_target_classes
from snack_and_lift.application.verification import get_my_bookings, verify_bookings
from snack_and_lift.domain.errors import GymError, NoBookingsFoundError, RetriesExhaustedError
from snack_and_lift.domain.models import ClassResult, Outcome


def test_get_my_bookings_opens_the_page_and_returns_all_entries() -> None:
    entries = [make_entry("Wed, Aug 13, 7:00 AM"), make_entry(waitlisted=True)]
    gym = FakeGym(bookings=entries)

    assert get_my_bookings(gym) == entries
    assert gym.calls == ["open_my_bookings", "list_my_bookings"]


def test_get_my_bookings_raises_when_the_page_has_no_entry() -> None:
    with pytest.raises(NoBookingsFoundError):
        get_my_bookings(FakeGym(bookings=[]))


def test_get_my_bookings_propagates_the_page_error() -> None:
    with pytest.raises(GymError, match="Failed to load"):
        get_my_bookings(FakeGym(bookings_error="Failed to load bookings"))


def test_verify_bookings_succeeds_for_the_booked_classes() -> None:
    gym = FakeGym(
        cards=[
            make_card("Tue, Aug 12", card_id="1"),
            make_card("Thu, Aug 14", card_id="2", button_text="Join Waitlist"),
        ]
    )
    results = book_target_classes(gym)

    verification = verify_bookings(gym, results)

    assert verification.is_success
    assert verification.verified == ["Spin Class", "Spin Class (Waitlist)"]


def test_verify_bookings_ignores_entries_that_are_not_target_classes() -> None:
    gym = FakeGym(bookings=[make_entry(), make_entry("Wed, Aug 13, 6:00 PM")])
    results = [ClassResult(make_card("Tue, Aug 12"), Outcome.NEW_BOOKING)]

    assert verify_bookings(gym, results).is_success


def test_verify_bookings_lists_target_entries_after_the_window_as_also_booked() -> None:
    gym = FakeGym(bookings=[make_entry(), make_entry("Thu, Aug 21, 6:00 PM")])
    results = [ClassResult(make_card("Tue, Aug 12"), Outcome.NEW_BOOKING)]

    verification = verify_bookings(gym, results)

    assert verification.is_success
    assert verification.also_booked == ["Spin Class on Thu, Aug 21"]


def test_verify_bookings_reports_a_missing_booking() -> None:
    gym = FakeGym(bookings=[make_entry("Wed, Aug 13, 7:00 AM")])
    results = [ClassResult(make_card("Tue, Aug 12"), Outcome.NEW_BOOKING)]

    verification = verify_bookings(gym, results)

    assert not verification.is_success
    assert verification.missing == ["Spin Class on Tue, Aug 12"]


def test_verify_bookings_raises_when_classes_were_booked_but_the_page_is_empty() -> None:
    gym = FakeGym(bookings=[])
    results = [ClassResult(make_card("Tue, Aug 12"), Outcome.NEW_BOOKING)]

    with pytest.raises(RetriesExhaustedError) as caught:
        verify_bookings(gym, results, sleep=no_sleep)

    assert isinstance(caught.value.__cause__, NoBookingsFoundError)


def test_verify_bookings_skips_the_page_when_nothing_is_expected() -> None:
    gym = FakeGym()

    verification = verify_bookings(gym, [])

    assert verification.is_success
    assert verification.expected == 0
    assert gym.calls == []
