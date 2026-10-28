"""@file verification.py
@brief Lecture steps 7 and 8: compare what the bot did with the My Bookings page.
"""

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

from snack_and_lift import constants
from snack_and_lift.domain.booking_entry import BookingEntry
from snack_and_lift.domain.errors import PageFormatError
from snack_and_lift.domain.models import ClassResult, Outcome

_WAITLISTED_OUTCOMES = (Outcome.NEW_WAITLIST, Outcome.ALREADY_WAITLISTED)

## An entry is identified by its class name, its date text and whether it is waitlisted.
_Key = tuple[str, str, bool]


@dataclass(frozen=True, slots=True)
class VerificationResult:
    """@brief What the My Bookings page shows compared with what the bot did.

    `verified`, `missing`, `unexpected` and `also_booked` hold display names, with the waitlist
    suffix for a waitlist entry; all but `verified` also say the day (`Spin Class on Tue, Aug 12`).
    Only entries from the earliest to the latest class the bot handled are checked: `found`
    counts them, and `also_booked` lists the entries outside that window, which never cause
    a mismatch.
    """

    expected: int
    found: int
    verified: list[str]
    missing: list[str]
    unexpected: list[str]
    also_booked: list[str]

    @property
    def is_success(self) -> bool:
        """@brief True when every expected entry was found and nothing else was."""
        return self.expected == self.found and not self.missing and not self.unexpected


def _display_name(name: str, waitlisted: bool) -> str:
    """@brief The name as the page shows it."""
    return name + constants.WAITLIST_NAME_SUFFIX if waitlisted else name


def _expected_keys(results: Sequence[ClassResult]) -> list[_Key]:
    """@brief The entries the bot's results say must be on the page."""
    return [(r.card.name, r.card.date_text, r.outcome in _WAITLISTED_OUTCOMES) for r in results]


def _entry_keys(entries: Sequence[BookingEntry]) -> list[_Key]:
    """@brief The identity of each entry found on the page."""
    return [(e.name, e.date_text, e.waitlisted) for e in entries]


def _describe(key: _Key) -> str:
    """@brief Write an entry for the missing and unexpected lines."""
    name, day, waitlisted = key
    return f"{_display_name(name, waitlisted)} on {day}"


def _day_number(date_text: str) -> int:
    """@brief The position of a date (`Tue, Aug 12`) in a year; the page shows no year.

    @exception PageFormatError The text has no valid month and day.
    """
    month_text, _, day_text = date_text.partition(", ")[2].partition(" ")
    try:
        month = constants.MONTH_ABBREVIATIONS.index(month_text) + 1
        day = date(constants.DATE_CYCLE_YEAR, month, int(day_text))
    except ValueError as error:
        raise PageFormatError(f"Unexpected date: {date_text!r}") from error
    return day.timetuple().tm_yday


def _offset(day: int, start: int) -> int:
    """@brief The days from `start` to `day`, counting over the turn of the year."""
    return (day - start) % constants.DAYS_IN_DATE_CYCLE


def _window(keys: Sequence[_Key]) -> tuple[int, int] | None:
    """@brief The first day and the length in days of the shortest span holding all the keys.

    @return None when there is no key.
    """
    days = [_day_number(key[1]) for key in keys]
    spans = [(max(_offset(day, start) for day in days), start) for start in days]
    if not spans:
        return None
    span, start = min(spans)
    return start, span


def _is_in_window(key: _Key, window: tuple[int, int] | None) -> bool:
    """@brief Tell whether the date of the key lies in the window, ends included."""
    if window is None:
        return False
    start, span = window
    return _offset(_day_number(key[1]), start) <= span


def build_verification(
    results: Sequence[ClassResult], entries: Sequence[BookingEntry]
) -> VerificationResult:
    """@brief Compare the results of the booking with the target entries of the page.

    @param results What happened to each class; waitlisted when the outcome is a waitlist one.
    @param entries The Tuesday and Thursday 6pm entries found on the page.
    @return The comparison; only the entries from the earliest to the latest class handled
        are checked, the others are `also_booked`, and no class handled means no check.
    @exception PageFormatError An entry or a card has no valid date.
    """
    expected = _expected_keys(results)
    window = _window(expected)
    keys = _entry_keys(entries)
    checked = [key for key in keys if _is_in_window(key, window)]
    also_booked = [_describe(key) for key in keys if not _is_in_window(key, window)]
    remaining = Counter(checked)
    verified: list[str] = []
    missing: list[str] = []
    for key in expected:
        if remaining[key] > 0:
            remaining[key] -= 1
            verified.append(_display_name(key[0], key[2]))
        else:
            missing.append(_describe(key))
    unexpected = [_describe(key) for key in remaining.elements()]
    return VerificationResult(
        len(expected), len(checked), verified, missing, unexpected, also_booked
    )


def _count_text(template: str, count: int) -> str:
    """@brief Write a count with `booking` in the singular for 1."""
    noun = constants.VERIFY_NOUN_SINGULAR if count == 1 else constants.VERIFY_NOUN_PLURAL
    return template.format(count=count, noun=noun)


def format_verification(result: VerificationResult) -> str:
    """@brief Write the verification block.

    @param result The comparison.
    @return The block, starting with `--- VERIFYING ON MY BOOKINGS PAGE ---`.
    """
    lines = [constants.VERIFY_TITLE]
    lines.extend(constants.VERIFY_LINE_VERIFIED.format(name=name) for name in result.verified)
    lines.append("")
    lines.append(constants.VERIFY_RESULT_TITLE)
    lines.append(_count_text(constants.VERIFY_EXPECTED, result.expected))
    lines.append(_count_text(constants.VERIFY_FOUND, result.found))
    lines.extend(constants.VERIFY_LINE_ALSO_BOOKED.format(entry=t) for t in result.also_booked)
    if result.is_success:
        lines.append(constants.VERIFY_SUCCESS)
        return "\n".join(lines)
    lines.append(constants.VERIFY_MISMATCH.format(count=len(result.missing)))
    lines.extend(constants.VERIFY_LINE_MISSING.format(entry=text) for text in result.missing)
    lines.extend(constants.VERIFY_LINE_UNEXPECTED.format(entry=text) for text in result.unexpected)
    return "\n".join(lines)
