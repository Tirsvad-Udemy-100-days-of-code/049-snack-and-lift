"""@file report.py
@brief Lecture steps 5 and 6: count what the bot did and write the summary and the class list.
"""

from collections.abc import Sequence
from dataclasses import dataclass

from snack_and_lift import constants
from snack_and_lift.domain.models import ClassResult, Outcome

_TAG_OF_OUTCOME: dict[Outcome, str] = {
    Outcome.NEW_BOOKING: constants.DETAIL_TAG_NEW_BOOKING,
    Outcome.NEW_WAITLIST: constants.DETAIL_TAG_NEW_WAITLIST,
    Outcome.ALREADY_BOOKED: constants.DETAIL_TAG_ALREADY_BOOKED,
    Outcome.ALREADY_WAITLISTED: constants.DETAIL_TAG_ALREADY_WAITLISTED,
}

_ALREADY_DONE = (Outcome.ALREADY_BOOKED, Outcome.ALREADY_WAITLISTED)


@dataclass(frozen=True, slots=True)
class Counters:
    """@brief How many classes ended in each way."""

    new_bookings: int
    new_waitlist: int
    already_done: int

    @property
    def total(self) -> int:
        """@brief The number of classes handled."""
        return self.new_bookings + self.new_waitlist + self.already_done


def count_results(results: Sequence[ClassResult]) -> Counters:
    """@brief Count the results by outcome.

    @param results What happened to each class.
    @return The counters; already booked and already waitlisted count together.
    """
    return Counters(
        new_bookings=sum(1 for r in results if r.outcome is Outcome.NEW_BOOKING),
        new_waitlist=sum(1 for r in results if r.outcome is Outcome.NEW_WAITLIST),
        already_done=sum(1 for r in results if r.outcome in _ALREADY_DONE),
    )


def format_summary(results: Sequence[ClassResult]) -> str:
    """@brief Write the booking summary block.

    @param results What happened to each class.
    @return The block, starting with `--- BOOKING SUMMARY ---`, lines joined by newlines.
    """
    counters = count_results(results)
    return "\n".join(
        [
            constants.SUMMARY_TITLE,
            constants.SUMMARY_NEW_BOOKINGS.format(count=counters.new_bookings),
            constants.SUMMARY_NEW_WAITLIST.format(count=counters.new_waitlist),
            constants.SUMMARY_ALREADY_DONE.format(count=counters.already_done),
            constants.SUMMARY_TOTAL.format(count=counters.total),
        ]
    )


def format_detail_list(results: Sequence[ClassResult]) -> str:
    """@brief Write the detailed class list, one line per class in the order handled.

    @param results What happened to each class.
    @return The block, starting with `--- DETAILED CLASS LIST ---`; says so when empty.
    """
    lines = [constants.DETAIL_TITLE]
    if not results:
        lines.append(constants.DETAIL_NONE)
    lines.extend(
        constants.DETAIL_LINE.format(
            tag=_TAG_OF_OUTCOME[result.outcome], name=result.card.name, day=result.card.day_label
        )
        for result in results
    )
    return "\n".join(lines)
