"""@file fakes.py
@brief A fake of the GymPort for the unit tests.
"""

import random
from dataclasses import replace
from pathlib import Path

from snack_and_lift import constants
from snack_and_lift.domain.booking_entry import BookingEntry
from snack_and_lift.domain.errors import GymError, LoginFailedError
from snack_and_lift.domain.models import ButtonState, ClassCard

_PRESS_RESULTS = {
    constants.BUTTON_TEXT_BOOK: constants.BUTTON_TEXT_BOOKED,
    constants.BUTTON_TEXT_JOIN_WAITLIST: constants.BUTTON_TEXT_WAITLISTED,
}


_WAITLISTED_BY_STATE = {
    ButtonState.BOOK: False,
    ButtonState.BOOKED: False,
    ButtonState.JOIN_WAITLIST: True,
    ButtonState.WAITLISTED: True,
}


def _entry_of(card: ClassCard) -> BookingEntry | None:
    """@brief The My Bookings entry that a card ends in, or None when it is not booked."""
    flag = _WAITLISTED_BY_STATE.get(card.state)
    if flag is None:
        return None
    time_text = card.time_text.removeprefix(constants.TIME_TEXT_PREFIX).strip()
    return BookingEntry(card.name, f"{card.date_text}, {time_text}", flag)


NETWORK_ERROR_TEXT = "Network request failed. Please try again."


class FakeGym:
    """@brief Records the calls; can refuse the login, serve cards and fail a click.

    Unless `bookings` is given, the My Bookings page shows every card that is, or by the
    click becomes, booked or waitlisted. A successful click turns the card's button into its
    new state, so a card read again shows what the click did.

    `fail_first` is a deterministic failure schedule: it maps the name of a port method
    (`log_in`, `press_class_button`, `open_my_bookings`, `list_my_bookings`) to the number of
    its first calls that fail like a dropped request. With `click_goes_through`, a failing
    `press_class_button` still turns the button (the click arrived, the answer did not).
    """

    def __init__(
        self,
        login_error: str | None = None,
        cards: list[ClassCard] | None = None,
        press_result: str | None = None,
        press_error: str | None = None,
        bookings: list[BookingEntry] | None = None,
        bookings_error: str | None = None,
        fail_first: dict[str, int] | None = None,
        click_goes_through: bool = False,
    ) -> None:
        self.login_error = login_error
        self.cards = cards or []
        self.press_result = press_result
        self.press_error = press_error
        self.bookings = bookings
        self.bookings_error = bookings_error
        self.click_goes_through = click_goes_through
        self._failures_left = dict(fail_first or {})
        self.calls: list[str] = []
        self.logins: list[tuple[str, str]] = []
        self.screenshots: list[Path] = []
        self.text_screenshots: list[tuple[str, Path]] = []
        self.pressed: list[str] = []
        self.closed = False

    def open_site(self) -> None:
        self.calls.append("open_site")

    def _should_fail(self, name: str) -> bool:
        """@brief Whether this call is one of the scheduled failures; counts it."""
        left = self._failures_left.get(name, 0)
        if left > 0:
            self._failures_left[name] = left - 1
            return True
        return False

    def _turn_button(self, card_id: str) -> str:
        """@brief Turn the button of a card to the state its click gives; return the new text."""
        index = next(i for i, card in enumerate(self.cards) if card.card_id == card_id)
        card = self.cards[index]
        new_text = _PRESS_RESULTS[card.button_text]
        self.cards[index] = replace(card, button_text=new_text)
        return new_text

    def log_in(self, email: str, password: str) -> None:
        self.calls.append("log_in")
        self.logins.append((email, password))
        if self.login_error is not None:
            raise LoginFailedError(self.login_error)
        if self._should_fail("log_in"):
            raise LoginFailedError(NETWORK_ERROR_TEXT)

    def list_class_cards(self) -> list[ClassCard]:
        self.calls.append("list_class_cards")
        return list(self.cards)

    def press_class_button(self, card_id: str) -> str:
        self.calls.append("press_class_button")
        self.pressed.append(card_id)
        if self.press_error is not None:
            raise GymError(self.press_error)
        if self.press_result is not None:
            return self.press_result
        if self._should_fail("press_class_button"):
            if self.click_goes_through:
                self._turn_button(card_id)
            raise GymError(NETWORK_ERROR_TEXT)
        return self._turn_button(card_id)

    def open_my_bookings(self) -> None:
        self.calls.append("open_my_bookings")
        if self._should_fail("open_my_bookings"):
            raise GymError(NETWORK_ERROR_TEXT)

    def list_my_bookings(self) -> list[BookingEntry]:
        self.calls.append("list_my_bookings")
        if self._should_fail("list_my_bookings"):
            raise GymError(NETWORK_ERROR_TEXT)
        if self.bookings_error is not None:
            raise GymError(self.bookings_error)
        if self.bookings is not None:
            return list(self.bookings)
        entries = (_entry_of(card) for card in self.cards)
        return [entry for entry in entries if entry is not None]

    def save_text_screenshot(self, text: str, path: Path) -> None:
        self.calls.append("save_text_screenshot")
        self.text_screenshots.append((text, path))

    def save_screenshot(self, path: Path) -> None:
        self.calls.append("save_screenshot")
        self.screenshots.append(path)

    def close(self) -> None:
        self.calls.append("close")
        self.closed = True


class ChaosGym(FakeGym):
    """@brief A gym whose login, click and bookings read each fail with a set probability.

    The site's network simulation fails up to 50% of these requests and writes nothing when
    one fails. The random numbers come from a seeded generator, so a run is repeatable.
    """

    _FAILING_CALLS = frozenset({"log_in", "press_class_button", "list_my_bookings"})

    def __init__(
        self,
        rng: random.Random,
        failure_probability: float = 0.5,
        cards: list[ClassCard] | None = None,
    ) -> None:
        super().__init__(cards=cards)
        self._rng = rng
        self._failure_probability = failure_probability

    def _should_fail(self, name: str) -> bool:
        return name in self._FAILING_CALLS and self._rng.random() < self._failure_probability


def no_sleep(seconds: float) -> None:
    """@brief A `sleep` that returns at once, so a retry test never waits."""
