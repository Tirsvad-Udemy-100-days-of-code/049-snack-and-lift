"""@file models.py
@brief Plain data of the schedule: the button state, a class card and the result of a booking.
"""

from dataclasses import dataclass
from enum import Enum, auto

from snack_and_lift import constants
from snack_and_lift.domain.day_label import parse_day_label


class ButtonState(Enum):
    """@brief What the button of a class card says."""

    BOOK = auto()
    JOIN_WAITLIST = auto()
    BOOKED = auto()
    WAITLISTED = auto()
    BUSY = auto()
    COMPLETED = auto()
    UNKNOWN = auto()

    @classmethod
    def from_text(cls, text: str) -> "ButtonState":
        """@brief Map the text of a button to its state.

        @param text The visible text of the button (or the label of a past class).
        @return The state; UNKNOWN for a text the bot does not know.
        """
        return _STATE_BY_TEXT.get(text.strip(), cls.UNKNOWN)


_STATE_BY_TEXT: dict[str, ButtonState] = {
    constants.BUTTON_TEXT_BOOK: ButtonState.BOOK,
    constants.BUTTON_TEXT_JOIN_WAITLIST: ButtonState.JOIN_WAITLIST,
    constants.BUTTON_TEXT_BOOKED: ButtonState.BOOKED,
    constants.BUTTON_TEXT_WAITLISTED: ButtonState.WAITLISTED,
    constants.BUTTON_TEXT_BOOKING: ButtonState.BUSY,
    constants.BUTTON_TEXT_JOINING: ButtonState.BUSY,
    constants.BUTTON_TEXT_COMPLETED: ButtonState.COMPLETED,
}


@dataclass(frozen=True, slots=True)
class ClassCard:
    """@brief One class of the schedule, as read from the page.

    `card_id` is the id of the card without the `class-card-` prefix (for example
    "123"); the site builds the ids of the card's other elements from the same suffix.
    """

    card_id: str
    name: str
    day_label: str
    time_text: str
    button_text: str

    @property
    def state(self) -> ButtonState:
        """@brief The state of the button."""
        return ButtonState.from_text(self.button_text)

    @property
    def weekday(self) -> str:
        """@brief The weekday of the day group (`Tue`).

        @exception PageFormatError The day label is not in a known form.
        """
        return parse_day_label(self.day_label)[0]

    @property
    def date_text(self) -> str:
        """@brief The date of the day group (`Tue, Aug 12`).

        @exception PageFormatError The day label is not in a known form.
        """
        return parse_day_label(self.day_label)[1]


class Outcome(Enum):
    """@brief What the booking did, or found, for a class."""

    NEW_BOOKING = auto()
    NEW_WAITLIST = auto()
    ALREADY_BOOKED = auto()
    ALREADY_WAITLISTED = auto()


@dataclass(frozen=True, slots=True)
class ClassResult:
    """@brief The class that was handled and what happened to it."""

    card: ClassCard
    outcome: Outcome
