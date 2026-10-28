"""@file verification.py
@brief Lecture steps 7 and 8: compare what the bot did with the My Bookings page.
"""

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

from snack_and_lift import constants
from snack_and_lift.domain.booking_entry import BookingEntry
from snack_and_lift.domain.models import ClassResult, Outcome

_WAITLISTED_OUTCOMES = (Outcome.NEW_WAITLIST, Outcome.ALREADY_WAITLISTED)

## An entry is identified by its class name, its date text and whether it is waitlisted.
_Key = tuple[str, str, bool]


@dataclass(frozen=True, slots=True)
class VerificationResult:
    """@brief What the My Bookings page shows compared with what the bot did.

    `verified`, `missing` and `unexpected` hold display names, with the waitlist suffix for a
    waitlist entry; `missing` and `unexpected` also say the day (`Spin Class on Tue, Aug 12`).
    """

    expected: int
    found: int
    verified: list[str]
    missing: list[str]
    unexpected: list[str]

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


def build_verification(
    results: Sequence[ClassResult], entries: Sequence[BookingEntry]
) -> VerificationResult:
    """@brief Compare the results of the booking with the target entries of the page.

    @param results What happened to each class; waitlisted when the outcome is a waitlist one.
    @param entries The Tuesday and Thursday 6pm entries found on the page.
    @return The comparison; the counts are the numbers of results and of entries.
    @exception PageFormatError An entry or a card has no valid date.
    """
    expected = _expected_keys(results)
    remaining = Counter(_entry_keys(entries))
    verified: list[str] = []
    missing: list[str] = []
    for key in expected:
        if remaining[key] > 0:
            remaining[key] -= 1
            verified.append(_display_name(key[0], key[2]))
        else:
            missing.append(_describe(key))
    unexpected = [_describe(key) for key in remaining.elements()]
    return VerificationResult(len(expected), len(entries), verified, missing, unexpected)


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
    if result.is_success:
        lines.append(constants.VERIFY_SUCCESS)
        return "\n".join(lines)
    lines.append(constants.VERIFY_MISMATCH.format(count=result.expected - result.found))
    lines.extend(constants.VERIFY_LINE_MISSING.format(entry=text) for text in result.missing)
    lines.extend(constants.VERIFY_LINE_UNEXPECTED.format(entry=text) for text in result.unexpected)
    return "\n".join(lines)
