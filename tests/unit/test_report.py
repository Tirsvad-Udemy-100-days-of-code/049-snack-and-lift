"""@file test_report.py
@brief The counters, the booking summary and the detailed class list.
"""

from tests.unit.test_models import make_card

from snack_and_lift.domain.models import ClassResult, Outcome
from snack_and_lift.domain.report import (
    Counters,
    count_results,
    format_detail_list,
    format_summary,
)


def make_result(outcome: Outcome, day_label: str = "Tue, Aug 19") -> ClassResult:
    return ClassResult(make_card(day_label), outcome)


def test_count_results_groups_the_outcomes() -> None:
    results = [
        make_result(Outcome.NEW_BOOKING),
        make_result(Outcome.NEW_BOOKING),
        make_result(Outcome.NEW_WAITLIST),
        make_result(Outcome.ALREADY_BOOKED),
        make_result(Outcome.ALREADY_WAITLISTED),
    ]

    counters = count_results(results)

    assert counters == Counters(new_bookings=2, new_waitlist=1, already_done=2)
    assert counters.total == 5


def test_count_results_is_zero_for_no_results() -> None:
    assert count_results([]).total == 0


def test_format_summary_matches_the_lecture() -> None:
    results = [
        make_result(Outcome.NEW_BOOKING, "Tomorrow (Thu, Aug 14)"),
        make_result(Outcome.NEW_WAITLIST),
    ]

    assert format_summary(results) == (
        "--- BOOKING SUMMARY ---\n"
        "New bookings: 1\n"
        "New waitlist entries: 1\n"
        "Already booked/waitlisted: 0\n"
        "Total Tuesday & Thursday 6pm classes: 2"
    )


def test_format_summary_for_no_results() -> None:
    assert format_summary([]).endswith("Total Tuesday & Thursday 6pm classes: 0")


def test_format_detail_list_matches_the_lecture() -> None:
    results = [
        make_result(Outcome.NEW_BOOKING, "Tomorrow (Thu, Aug 14)"),
        make_result(Outcome.NEW_WAITLIST),
    ]

    assert format_detail_list(results) == (
        "--- DETAILED CLASS LIST ---\n"
        "  • [New Booking] Spin Class on Tomorrow (Thu, Aug 14)\n"
        "  • [New Waitlist] Spin Class on Tue, Aug 19"
    )


def test_format_detail_list_tags_every_outcome() -> None:
    results = [
        make_result(Outcome.ALREADY_BOOKED),
        make_result(Outcome.ALREADY_WAITLISTED),
    ]

    lines = format_detail_list(results).splitlines()

    assert lines[1:] == [
        "  • [Already Booked] Spin Class on Tue, Aug 19",
        "  • [Already Waitlisted] Spin Class on Tue, Aug 19",
    ]


def test_format_detail_list_says_when_no_class_was_found() -> None:
    assert format_detail_list([]) == "--- DETAILED CLASS LIST ---\n  No matching class found"
