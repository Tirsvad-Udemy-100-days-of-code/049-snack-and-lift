"""@file test_verification.py
@brief The comparison of the bot's results with the My Bookings page, and its text.
"""

from tests.unit.test_booking_entry import make_entry
from tests.unit.test_models import make_card

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


def test_unexpected_entry_gives_a_negative_missing_count() -> None:
    result = build_verification(
        [BOOKED], [make_entry("Tue, Aug 12, 6:00 PM"), make_entry("Thu, Aug 14, 6:00 PM")]
    )

    text = format_verification(result)

    assert result.unexpected == ["Spin Class on Thu, Aug 14"]
    assert "❌ MISMATCH: Missing -1 bookings" in text
    assert text.endswith("  ? Unexpected: Spin Class on Thu, Aug 14")


def test_waitlist_flag_must_match() -> None:
    result = build_verification([BOOKED], [make_entry("Tue, Aug 12, 6:00 PM", waitlisted=True)])

    assert result.missing == ["Spin Class on Tue, Aug 12"]
    assert result.unexpected == ["Spin Class (Waitlist) on Tue, Aug 12"]
    assert "Missing 0 bookings" in format_verification(result)


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
