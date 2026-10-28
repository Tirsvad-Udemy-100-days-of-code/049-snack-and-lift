"""@file rules.py
@brief The booking rules: which class is the target, what to do for a button state, what to say.
"""

import re
from collections.abc import Iterable
from enum import Enum, auto

from snack_and_lift import constants
from snack_and_lift.domain.day_label import parse_day_label
from snack_and_lift.domain.errors import PageFormatError, UnknownButtonError
from snack_and_lift.domain.models import ButtonState, ClassCard, Outcome

__all__ = [
    "CONFIRMED_STATE",
    "OUTCOME_OF_ACTION",
    "Action",
    "decide_outcome_action",
    "find_next_class",
    "format_outcome",
    "is_target_time",
    "parse_day_label",
    "parse_time",
]

_TIME = re.compile(
    rf"(?:{re.escape(constants.TIME_TEXT_PREFIX)}\s*)?(\d{{1,2}}):(\d{{2}})\s*(AM|PM)",
    re.IGNORECASE,
)
_MAX_CLOCK_HOUR = 12
_MAX_MINUTE = 59


class Action(Enum):
    """@brief What the bot does for a class card."""

    CLICK_BOOK = auto()
    CLICK_WAITLIST = auto()
    ALREADY_BOOKED = auto()
    ALREADY_WAITLISTED = auto()


## The outcome that follows from each action.
OUTCOME_OF_ACTION: dict[Action, Outcome] = {
    Action.CLICK_BOOK: Outcome.NEW_BOOKING,
    Action.CLICK_WAITLIST: Outcome.NEW_WAITLIST,
    Action.ALREADY_BOOKED: Outcome.ALREADY_BOOKED,
    Action.ALREADY_WAITLISTED: Outcome.ALREADY_WAITLISTED,
}

## The button state that proves a click worked.
CONFIRMED_STATE: dict[Action, ButtonState] = {
    Action.CLICK_BOOK: ButtonState.BOOKED,
    Action.CLICK_WAITLIST: ButtonState.WAITLISTED,
}

_ACTION_OF_STATE: dict[ButtonState, Action] = {
    ButtonState.BOOK: Action.CLICK_BOOK,
    ButtonState.JOIN_WAITLIST: Action.CLICK_WAITLIST,
    ButtonState.BOOKED: Action.ALREADY_BOOKED,
    ButtonState.WAITLISTED: Action.ALREADY_WAITLISTED,
}

_MESSAGE_OF_OUTCOME: dict[Outcome, str] = {
    Outcome.NEW_BOOKING: constants.MESSAGE_BOOKED,
    Outcome.NEW_WAITLIST: constants.MESSAGE_WAITLISTED,
    Outcome.ALREADY_BOOKED: constants.MESSAGE_ALREADY_BOOKED,
    Outcome.ALREADY_WAITLISTED: constants.MESSAGE_ALREADY_WAITLISTED,
}


def parse_time(text: str) -> tuple[int, int]:
    """@brief Read a 12-hour time such as `6:00 PM`.

    @param text The time, with or without the `Time:` prefix.
    @return The hour (0-23) and the minute.
    @exception PageFormatError The text is not a valid time.
    """
    match = _TIME.fullmatch(text.strip())
    if match is None:
        raise PageFormatError(f"Unexpected time text: {text!r}")
    hour, minute = int(match[1]), int(match[2])
    if not 1 <= hour <= _MAX_CLOCK_HOUR or minute > _MAX_MINUTE:
        raise PageFormatError(f"Time out of range: {text!r}")
    hour %= _MAX_CLOCK_HOUR
    if match[3].upper() == "PM":
        hour += _MAX_CLOCK_HOUR
    return hour, minute


def is_target_time(card: ClassCard) -> bool:
    """@brief Tell whether the class starts at the time the bot books.

    @param card The class.
    @return True at `TARGET_HOUR`:`TARGET_MINUTE`.
    @exception PageFormatError The time text is not valid.
    """
    return parse_time(card.time_text) == (constants.TARGET_HOUR, constants.TARGET_MINUTE)


def find_next_class(cards: Iterable[ClassCard], weekday: str) -> ClassCard | None:
    """@brief Find the first class of a weekday at the target time, in page order.

    The weekday is read from each card's day label; the position in the list means nothing.
    Classes already completed are skipped.

    @param cards The classes in the order of the page.
    @param weekday The weekday as the site abbreviates it (`Tue`).
    @return The class, or None when there is none.
    """
    for card in cards:
        if card.state is ButtonState.COMPLETED:
            continue
        if card.weekday == weekday and is_target_time(card):
            return card
    return None


def decide_outcome_action(card: ClassCard) -> Action:
    """@brief Decide what to do from the state of the button.

    @param card The class.
    @return The action.
    @exception UnknownButtonError The button is busy, completed or unknown; `retry` can repeat.
    """
    action = _ACTION_OF_STATE.get(card.state)
    if action is None:
        raise UnknownButtonError(f"Cannot act on button {card.button_text!r} of {card.name}")
    return action


def format_outcome(outcome: Outcome, card: ClassCard) -> str:
    """@brief Build the console message of an outcome.

    @param outcome What happened.
    @param card The class; its day label is shown as the site writes it.
    @return For example `✓ Successfully booked: Spin Class on Tomorrow (Thu, Aug 14)`.
    """
    return _MESSAGE_OF_OUTCOME[outcome].format(name=card.name, day=card.day_label)
