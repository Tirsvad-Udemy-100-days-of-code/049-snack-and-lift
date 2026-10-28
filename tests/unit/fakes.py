"""@file fakes.py
@brief A fake of the GymPort for the unit tests.
"""

from pathlib import Path

from snack_and_lift import constants
from snack_and_lift.domain.errors import GymError, LoginFailedError
from snack_and_lift.domain.models import ClassCard

_PRESS_RESULTS = {
    constants.BUTTON_TEXT_BOOK: constants.BUTTON_TEXT_BOOKED,
    constants.BUTTON_TEXT_JOIN_WAITLIST: constants.BUTTON_TEXT_WAITLISTED,
}


class FakeGym:
    """@brief Records the calls; can refuse the login, serve cards and fail a click."""

    def __init__(
        self,
        login_error: str | None = None,
        cards: list[ClassCard] | None = None,
        press_result: str | None = None,
        press_error: str | None = None,
    ) -> None:
        self.login_error = login_error
        self.cards = cards or []
        self.press_result = press_result
        self.press_error = press_error
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

    def save_text_screenshot(self, text: str, path: Path) -> None:
        self.calls.append("save_text_screenshot")
        self.text_screenshots.append((text, path))

    def save_screenshot(self, path: Path) -> None:
        self.calls.append("save_screenshot")
        self.screenshots.append(path)

    def close(self) -> None:
        self.calls.append("close")
        self.closed = True
