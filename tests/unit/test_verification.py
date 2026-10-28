"""@file test_verification.py
@brief The comparison of the bot's results with the My Bookings page, and its text.
"""

import pytest
from tests.unit.test_booking_entry import make_entry
from tests.unit.test_models import make_card

from snack_and_lift.domain.errors import PageFormatError
from snack_and_lift.domain.models import ClassResult, Outcome
from snack_and_lift.domain.verification import build_verification, format_verification

BOOKED = ClassResult(make_card("Tue, Aug 12"), Outcome.NEW_BOOKING)
WAITLISTED = ClassResult(make_card("Thu, Aug 14", card_id="2"), Outcome.NEW_WAITLIST)


def test_everything_found_is_a_success() -> None:
    result = build_verification(
        [BOOKED, WAITLISTED],
        [make_entry("Tue, Aug 12, 6:00 PM"), make_entry("Thu, Aug 14, 6:00 PM", waitlisted=True)],
    )

    assert result.is_success
    assert result.verified == ["Spin Class", "Spin Class (Waitlist)"]
    assert (result.expected, result.found) == (2, 2)


def test_success_text_is_exact() -> None:
    result = build_verification(
        [BOOKED, WAITLISTED],
        [make_entry("Tue, Aug 12, 6:00 PM"), make_entry("Thu, Aug 14, 6:00 PM", waitlisted=True)],
    )

    assert format_verification(result) == (
        "--- VERIFYING ON MY BOOKINGS PAGE ---\n"
        "  ✓ Verified: Spin Class\n"
        "  ✓ Verified: Spin Class (Waitlist)\n"
        "\n"
        "--- VERIFICATION RESULT ---\n"
        "Expected: 2 bookings\n"
        "Found: 2 bookings\n"
        "✅ SUCCESS: All bookings verified!"
    )


def test_one_booking_is_singular() -> None:
    text = format_verification(build_verification([BOOKED], [make_entry("Tue, Aug 12, 6:00 PM")]))

    assert "Expected: 1 booking\nFound: 1 booking\n" in text


def test_missing_entry_is_a_mismatch_with_a_line() -> None:
    result = build_verification([BOOKED, WAITLISTED], [make_entry("Tue, Aug 12, 6:00 PM")])

    text = format_verification(result)

    assert not result.is_success
    assert result.missing == ["Spin Class (Waitlist) on Thu, Aug 14"]
    assert "Expected: 2 bookings\nFound: 1 booking\n❌ MISMATCH: Missing 1 bookings" in text
    assert text.endswith("  ✗ Missing: Spin Class (Waitlist) on Thu, Aug 14")


def test_unexpected_entry_inside_the_window_is_a_mismatch() -> None:
    result = build_verification(
        [BOOKED, WAITLISTED],
        [
            make_entry("Tue, Aug 12, 6:00 PM"),
            make_entry("Thu, Aug 14, 6:00 PM", waitlisted=True),
            make_entry("Thu, Aug 14, 6:00 PM", name="Yoga Class"),
        ],
    )

    text = format_verification(result)

    assert not result.is_success
    assert result.unexpected == ["Yoga Class on Thu, Aug 14"]
    assert "❌ MISMATCH: Missing 0 bookings" in text
    assert text.endswith("  ? Unexpected: Yoga Class on Thu, Aug 14")


def test_entries_outside_the_window_are_a_note_and_a_success() -> None:
    result = build_verification(
        [BOOKED, WAITLISTED],
        [
            make_entry("Tue, Aug 12, 6:00 PM"),
            make_entry("Thu, Aug 14, 6:00 PM", waitlisted=True),
            make_entry("Thu, Aug 7, 6:00 PM"),
            make_entry("Tue, Aug 19, 6:00 PM", waitlisted=True),
        ],
    )

    assert result.is_success
    assert (result.expected, result.found) == (2, 2)
    assert result.also_booked == [
        "Spin Class on Thu, Aug 7",
        "Spin Class (Waitlist) on Tue, Aug 19",
    ]
    assert format_verification(result) == (
        "--- VERIFYING ON MY BOOKINGS PAGE ---\n"
        "  ✓ Verified: Spin Class\n"
        "  ✓ Verified: Spin Class (Waitlist)\n"
        "\n"
        "--- VERIFICATION RESULT ---\n"
        "Expected: 2 bookings\n"
        "Found: 2 bookings\n"
        "  i Also booked (not checked): Spin Class on Thu, Aug 7\n"
        "  i Also booked (not checked): Spin Class (Waitlist) on Tue, Aug 19\n"
        "✅ SUCCESS: All bookings verified!"
    )


def test_window_ends_are_inclusive() -> None:
    result = build_verification(
        [BOOKED, WAITLISTED],
        [make_entry("Tue, Aug 12, 6:00 PM"), make_entry("Thu, Aug 14, 6:00 PM", waitlisted=True)],
    )

    assert result.also_booked == []


def test_missing_count_is_the_number_of_missing_classes_with_notes_outside() -> None:
    result = build_verification(
        [BOOKED, WAITLISTED],
        [make_entry("Tue, Aug 12, 6:00 PM"), make_entry("Tue, Aug 26, 6:00 PM")],
    )

    text = format_verification(result)

    assert result.missing == ["Spin Class (Waitlist) on Thu, Aug 14"]
    assert "Expected: 2 bookings\nFound: 1 booking\n" in text
    assert (
        "  i Also booked (not checked): Spin Class on Tue, Aug 26\n❌ MISMATCH: Missing 1 bookings"
        in text
    )


def test_missing_count_is_never_negative() -> None:
    result = build_verification(
        [BOOKED, WAITLISTED],
        [
            make_entry("Tue, Aug 12, 6:00 PM"),
            make_entry("Wed, Aug 13, 6:00 PM"),
            make_entry("Wed, Aug 13, 6:00 PM", name="Yoga Class"),
        ],
    )

    assert "Missing 1 bookings" in format_verification(result)
    assert len(result.unexpected) == 2


def test_real_run_with_bookings_after_the_window_is_a_success() -> None:
    first = ClassResult(make_card("Thu, Oct 29"), Outcome.ALREADY_BOOKED)
    second = ClassResult(make_card("Tue, Nov 3", card_id="2"), Outcome.ALREADY_BOOKED)
    entries = [
        make_entry("Thu, Oct 29, 6:00 PM"),
        make_entry("Tue, Nov 3, 6:00 PM"),
        make_entry("Thu, Nov 12, 6:00 PM"),
        make_entry("Tue, Nov 17, 6:00 PM"),
        make_entry("Tue, Nov 24, 6:00 PM"),
    ]

    result = build_verification([first, second], entries)

    assert result.is_success
    assert (result.expected, result.found) == (2, 2)
    assert result.also_booked == [
        "Spin Class on Thu, Nov 12",
        "Spin Class on Tue, Nov 17",
        "Spin Class on Tue, Nov 24",
    ]


def test_no_results_makes_every_entry_a_note_and_no_mismatch() -> None:
    result = build_verification([], [make_entry("Tue, Aug 12, 6:00 PM")])

    assert result.is_success
    assert (result.expected, result.found) == (0, 0)
    assert result.also_booked == ["Spin Class on Tue, Aug 12"]


def test_window_holds_over_the_turn_of_the_year() -> None:
    december = ClassResult(make_card("Tue, Dec 30"), Outcome.NEW_BOOKING)
    january = ClassResult(make_card("Thu, Jan 1", card_id="2"), Outcome.NEW_BOOKING)

    result = build_verification(
        [december, january],
        [
            make_entry("Tue, Dec 30, 6:00 PM"),
            make_entry("Thu, Jan 1, 6:00 PM"),
            make_entry("Thu, Jan 8, 6:00 PM"),
            make_entry("Thu, Dec 18, 6:00 PM"),
        ],
    )

    assert result.is_success
    assert result.also_booked == ["Spin Class on Thu, Jan 8", "Spin Class on Thu, Dec 18"]


def test_leap_day_is_a_valid_date() -> None:
    leap = ClassResult(make_card("Thu, Feb 29"), Outcome.NEW_BOOKING)

    assert build_verification([leap], [make_entry("Thu, Feb 29, 6:00 PM")]).is_success


@pytest.mark.parametrize("date_text", ["Tue, Foo 12", "Tue, Feb 30"])
def test_an_invalid_date_is_a_page_format_error(date_text: str) -> None:
    bad = ClassResult(make_card(date_text), Outcome.NEW_BOOKING)

    with pytest.raises(PageFormatError):
        build_verification([bad], [])


def test_waitlist_flag_must_match() -> None:
    result = build_verification([BOOKED], [make_entry("Tue, Aug 12, 6:00 PM", waitlisted=True)])

    assert result.missing == ["Spin Class on Tue, Aug 12"]
    assert result.unexpected == ["Spin Class (Waitlist) on Tue, Aug 12"]
    assert "Missing 1 bookings" in format_verification(result)


def test_date_must_match() -> None:
    result = build_verification([BOOKED], [make_entry("Tue, Aug 19, 6:00 PM")])

    assert not result.is_success


def test_already_waitlisted_is_expected_as_waitlist() -> None:
    results = [ClassResult(make_card("Thu, Aug 14"), Outcome.ALREADY_WAITLISTED)]

    assert build_verification(
        results, [make_entry("Thu, Aug 14, 6:00 PM", waitlisted=True)]
    ).is_success


def test_nothing_expected_and_nothing_found_is_a_success() -> None:
    result = build_verification([], [])

    assert result.is_success
    assert "Expected: 0 bookings\nFound: 0 bookings\n✅ SUCCESS" in format_verification(result)


def test_same_class_twice_is_matched_one_to_one() -> None:
    result = build_verification([BOOKED, BOOKED], [make_entry("Tue, Aug 12, 6:00 PM")])

    assert result.verified == ["Spin Class"]
    assert result.missing == ["Spin Class on Tue, Aug 12"]
