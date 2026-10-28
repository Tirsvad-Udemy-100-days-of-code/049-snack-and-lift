"""@file fakes.py
@brief A fake of the GymPort for the unit tests.
"""

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


class FakeGym:
    """@brief Records the calls; can refuse the login, serve cards and fail a click.

    Unless `bookings` is given, the My Bookings page shows every card that is, or by the
    click becomes, booked or waitlisted.
    """

    def __init__(
        self,
        login_error: str | None = None,
        cards: list[ClassCard] | None = None,
        press_result: str | None = None,
        press_error: str | None = None,
        bookings: list[BookingEntry] | None = None,
        bookings_error: str | None = None,
    ) -> None:
        self.login_error = login_error
        self.cards = cards or []
        self.press_result = press_result
        self.press_error = press_error
        self.bookings = bookings
        self.bookings_error = bookings_error
        self.calls: list[str] = []
        self.logins: list[tuple[str, str]] = []
        self.screenshots: list[Path] = []
        self.text_screenshots: list[tuple[str, Path]] = []
        self.pressed: list[str] = []
        self.closed = False

    def open_site(self) -> None:
        self.calls.append("open_site")

    def log_in(self, email: str, password: str) -> None:
        self.calls.append("log_in")
        self.logins.append((email, password))
        if self.login_error is not None:
            raise LoginFailedError(self.login_error)

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
        card = next(card for card in self.cards if card.card_id == card_id)
        return _PRESS_RESULTS[card.button_text]

    def open_my_bookings(self) -> None:
        self.calls.append("open_my_bookings")

    def list_my_bookings(self) -> list[BookingEntry]:
        self.calls.append("list_my_bookings")
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
