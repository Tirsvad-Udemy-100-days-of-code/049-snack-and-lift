"""@file booking.py
@brief Lecture steps 3 to 6: book the Tuesday and Thursday 6pm classes and report their state.
"""

import logging
import time
from collections.abc import Callable

from snack_and_lift import constants
from snack_and_lift.application.ports import GymPort
from snack_and_lift.application.retry import Sleep, retry
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


def _read_current_card(gym: GymPort, card: ClassCard) -> ClassCard:
    """@brief Read a class again from the page, to see what an earlier attempt did.

    @param gym The gym site.
    @param card The class, as it was read before.
    @return The class with the state the page shows now.
    @exception GymError The schedule could not be read or the class is no longer on it.
    """
    for current in gym.list_class_cards():
        if current.card_id == card.card_id:
            return current
    raise GymError(constants.MESSAGE_CLASS_NOT_ON_SCHEDULE.format(card_id=card.card_id))


def book_class_with_retry(
    gym: GymPort,
    card: ClassCard,
    retries: int = constants.RETRY_COUNT,
    sleep: Sleep = time.sleep,
) -> ClassResult:
    """@brief Book a class, repeating it when the site drops the request.

    Before each repeat the class is read from the page again. When the button now shows the
    state that the click should give, the click did go through although its confirmation
    failed, so the class counts as newly booked or waitlisted and is not clicked again.

    @param gym The gym site.
    @param card The class, as read from the page.
    @param retries The most attempts to make.
    @param sleep Waits between two attempts.
    @return The class and what happened.
    @exception RetriesExhaustedError Every attempt failed.
    """
    attempts = 0

    def attempt() -> ClassResult:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return book_class(gym, card)
        current = _read_current_card(gym, card)
        action = decide_outcome_action(card)
        if CONFIRMED_STATE.get(action) is current.state:
            outcome = OUTCOME_OF_ACTION[action]
            logger.info(format_outcome(outcome, card))
            return ClassResult(card, outcome)
        return book_class(gym, current)

    description = constants.RETRY_DESCRIPTION_BOOK.format(name=card.name, day=card.day_label)
    return retry(attempt, retries, description, sleep=sleep)


def book_next_tuesday(
    gym: GymPort, retries: int = constants.RETRY_COUNT, sleep: Sleep = time.sleep
) -> ClassResult | None:
    """@brief Book the next Tuesday class at the target time.

    @param gym The gym site.
    @param retries The most attempts to book the class.
    @param sleep Waits between two attempts.
    @return The result, or None when the schedule has no such class.
    @exception GymError The page could not be read or the booking failed on every attempt.
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
    return book_class_with_retry(gym, card, retries, sleep)


def book_target_classes(
    gym: GymPort,
    on_result: Callable[[ClassResult], None] | None = None,
    retries: int = constants.RETRY_COUNT,
    sleep: Sleep = time.sleep,
) -> list[ClassResult]:
    """@brief Book every Tuesday and Thursday class at the target time, in page order.

    The cards are listed once; each class is found again by its id when it is pressed.

    @param gym The gym site.
    @param on_result Called after each class was handled, for example to take a screenshot.
    @param retries The most attempts to book one class.
    @param sleep Waits between two attempts.
    @return What happened to each class; empty when the schedule has none.
    @exception GymError The page could not be read or a booking failed on every attempt.
    """
    cards = find_target_classes(gym.list_class_cards())
    if not cards:
        logger.warning(constants.MESSAGE_NO_TARGET_CLASSES.format(time=constants.TARGET_TIME_TEXT))
        return []
    results: list[ClassResult] = []
    for card in cards:
        result = book_class_with_retry(gym, card, retries, sleep)
        results.append(result)
        if on_result is not None:
            on_result(result)
    return results
