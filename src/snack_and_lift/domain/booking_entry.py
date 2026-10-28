"""@file booking_entry.py
@brief One entry of the My Bookings page: a confirmed booking or a waitlist entry.
"""

import re
from dataclasses import dataclass

from snack_and_lift import constants
from snack_and_lift.domain.day_label import parse_day_label
from snack_and_lift.domain.errors import PageFormatError
from snack_and_lift.domain.rules import parse_time

_WHEN = re.compile(r"(?P<date>[A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}), (?P<time>.+)")


@dataclass(frozen=True, slots=True)
class BookingEntry:
    """@brief A booking or waitlist entry, as read from the My Bookings page.

    `name` is the class name WITHOUT the ` (Waitlist)` suffix the page adds to a waitlist
    entry; `waitlisted` carries that fact. `when_text` is the page text without the
    `When:` prefix, for example `Tue, Aug 12, 6:00 PM`.
    """

    name: str
    when_text: str
    waitlisted: bool

    @classmethod
    def from_page(cls, heading: str, when_text: str, waitlisted: bool) -> "BookingEntry":
        """@brief Build an entry from the texts of its card.

        @param heading The class name as the page shows it, possibly with the waitlist suffix.
        @param when_text The date and time paragraph, with or without the `When:` prefix.
        @param waitlisted True for a card of the waitlist section.
        @return The entry, with the suffix and the prefix removed.
        """
        name = heading.strip().removesuffix(constants.WAITLIST_NAME_SUFFIX.strip()).strip()
        when = when_text.strip().removeprefix(constants.WHEN_TEXT_PREFIX).strip()
        return cls(name, when, waitlisted)

    def _split_when(self) -> tuple[str, str]:
        """@brief Split the date text from the time text.

        @return The date text (`Tue, Aug 12`) and the time text (`6:00 PM`).
        @exception PageFormatError The text has no date and time.
        """
        match = _WHEN.fullmatch(self.when_text)
        if match is None:
            raise PageFormatError(f"Unexpected booking date and time: {self.when_text!r}")
        return match["date"], match["time"]

    @property
    def weekday(self) -> str:
        """@brief The weekday of the entry (`Tue`).

        @exception PageFormatError The date and time text is not valid.
        """
        return parse_day_label(self._split_when()[0])[0]

    @property
    def date_text(self) -> str:
        """@brief The date of the entry (`Tue, Aug 12`), comparable with a class card's date.

        @exception PageFormatError The date and time text is not valid.
        """
        return parse_day_label(self._split_when()[0])[1]

    @property
    def time(self) -> tuple[int, int]:
        """@brief The hour (0-23) and the minute of the entry.

        @exception PageFormatError The date and time text is not valid.
        """
        return parse_time(self._split_when()[1])


def is_target_entry(entry: BookingEntry) -> bool:
    """@brief Tell whether the entry is a class the bot books: a target weekday at the target time.

    @param entry The entry.
    @return True for Tuesday or Thursday at `TARGET_HOUR`:`TARGET_MINUTE`.
    @exception PageFormatError The date and time text is not valid.
    """
    return entry.weekday in constants.TARGET_WEEKDAYS and entry.time == (
        constants.TARGET_HOUR,
        constants.TARGET_MINUTE,
    )
