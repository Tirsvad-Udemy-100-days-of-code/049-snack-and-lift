"""@file test_booking_entry.py
@brief The entries of the My Bookings page: parsing and the target test.
"""

import dataclasses

import pytest

from snack_and_lift.domain.booking_entry import BookingEntry, is_target_entry
from snack_and_lift.domain.errors import GymError, NoBookingsFoundError, PageFormatError


def make_entry(
    when_text: str = "Tue, Aug 12, 6:00 PM", name: str = "Spin Class", waitlisted: bool = False
) -> BookingEntry:
    return BookingEntry(name, when_text, waitlisted)


def test_entry_derives_weekday_date_and_time() -> None:
    entry = make_entry("Thu, Aug 14, 6:00 PM")

    assert entry.weekday == "Thu"
    assert entry.date_text == "Thu, Aug 14"
    assert entry.time == (18, 0)


@pytest.mark.parametrize(
    "when_text", ["", "Someday", "Tue, Aug 12", "Tue, Aug 12, noon", "6:00 PM"]
)
def test_entry_with_bad_when_text_raises(when_text: str) -> None:
    with pytest.raises(PageFormatError):
        is_target_entry(make_entry(when_text))


def test_from_page_removes_the_waitlist_suffix_and_the_when_prefix() -> None:
    entry = BookingEntry.from_page("Spin Class (Waitlist)", "When: Tue, Aug 12, 6:00 PM", True)

    assert entry == BookingEntry("Spin Class", "Tue, Aug 12, 6:00 PM", True)


def test_from_page_keeps_a_plain_name() -> None:
    assert BookingEntry.from_page("Spin Class", "Tue, Aug 12, 6:00 PM", False).name == "Spin Class"


@pytest.mark.parametrize(
    ("when_text", "expected"),
    [
        ("Tue, Aug 12, 6:00 PM", True),
        ("Thu, Aug 14, 6:00 PM", True),
        ("Wed, Aug 13, 6:00 PM", False),
        ("Tue, Aug 12, 6:00 AM", False),
        ("Thu, Aug 14, 6:30 PM", False),
    ],
)
def test_is_target_entry(when_text: str, expected: bool) -> None:
    assert is_target_entry(make_entry(when_text)) is expected


def test_entry_is_immutable() -> None:
    with pytest.raises(dataclasses.FrozenInstanceError):
        make_entry().name = "Other"  # type: ignore[misc]


def test_no_bookings_found_is_a_gym_error() -> None:
    assert issubclass(NoBookingsFoundError, GymError)
