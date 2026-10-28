"""@file booking.py
@brief Lecture steps 3 to 6: book the Tuesday and Thursday 6pm classes and report their state.
"""

import logging
from collections.abc import Callable

from snack_and_lift import constants
from snack_and_lift.application.ports import GymPort
from snack_and_lift.domain.errors import GymError
from snack_and_lift.domain.models import ButtonState, ClassCard, ClassResult
from snack_and_lift.domain.rules import (
    CONFIRMED_STATE,
    OUTCOME_OF_ACTION,
    decide_outcome_action,
    find_next_class,
    find_target_classes,
    format_outcome,
)

logger = logging.getLogger(__name__)


def book_class(gym: GymPort, card: ClassCard) -> ClassResult:
    """@brief Book or waitlist a class, or report that it already is.

    @param gym The gym site.
    @param card The class, as read from the page.
    @return The class and what happened.
    @exception UnknownButtonError The button is busy, completed or unknown.
    @exception GymError The click failed or was not confirmed by the button.
    """
    action = decide_outcome_action(card)
    expected = CONFIRMED_STATE.get(action)
    if expected is not None:
        new_text = gym.press_class_button(card.card_id)
        if ButtonState.from_text(new_text) is not expected:
            raise GymError(f"click not confirmed: the button says {new_text!r}")
    outcome = OUTCOME_OF_ACTION[action]
    logger.info(format_outcome(outcome, card))
    return ClassResult(card, outcome)


def book_next_tuesday(gym: GymPort) -> ClassResult | None:
    """@brief Book the next Tuesday class at the target time.

    @param gym The gym site.
    @return The result, or None when the schedule has no such class.
    @exception GymError The page could not be read or the booking failed.
    """
    card = find_next_class(gym.list_class_cards(), constants.NEXT_CLASS_WEEKDAY)
    if card is None:
        logger.warning(
            constants.MESSAGE_NO_CLASS_FOUND.format(
                weekday=constants.NEXT_CLASS_WEEKDAY,
                time=constants.TARGET_TIME_TEXT,
            )
        )
        return None
    return book_class(gym, card)


def book_target_classes(
    gym: GymPort, on_result: Callable[[ClassResult], None] | None = None
) -> list[ClassResult]:
    """@brief Book every Tuesday and Thursday class at the target time, in page order.

    The cards are listed once; each class is found again by its id when it is pressed.

    @param gym The gym site.
    @param on_result Called after each class was handled, for example to take a screenshot.
    @return What happened to each class; empty when the schedule has none.
    @exception GymError The page could not be read or a booking failed.
    """
    cards = find_target_classes(gym.list_class_cards())
    if not cards:
        logger.warning(constants.MESSAGE_NO_TARGET_CLASSES.format(time=constants.TARGET_TIME_TEXT))
        return []
    results: list[ClassResult] = []
    for card in cards:
        result = book_class(gym, card)
        results.append(result)
        if on_result is not None:
            on_result(result)
    return results
