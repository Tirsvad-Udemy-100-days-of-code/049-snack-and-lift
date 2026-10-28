"""@file ports.py
@brief The ports the use cases need from the outside world.
"""

from pathlib import Path
from typing import Protocol

from snack_and_lift.domain.booking_entry import BookingEntry
from snack_and_lift.domain.models import ClassCard


class GymPort(Protocol):
    """@brief The gym site as the use cases see it."""

    def open_site(self) -> None:
        """@brief Open the home page and wait until it is ready.

        @exception GymError The page did not load.
        """
        ...

    def log_in(self, email: str, password: str) -> None:
        """@brief Log in and wait until the class schedule is shown.

        @param email The account e-mail.
        @param password The account password.
        @exception LoginFailedError The site refused the login.
        @exception GymError The page did not behave as expected.
        """
        ...

    def list_class_cards(self) -> list[ClassCard]:
        """@brief Read every class card of the schedule, in page order.

        @return The classes, each with the day of its group.
        @exception GymError The schedule could not be read.
        """
        ...

    def press_class_button(self, card_id: str) -> str:
        """@brief Click the button of a class and wait until the request has finished.

        @param card_id The id of the card without its prefix.
        @return The new text of the button.
        @exception GymError The site shows an error for the class (the message is its text)
            or nothing settled in time.
        """
        ...

    def open_my_bookings(self) -> None:
        """@brief Open the My Bookings page and wait until it is shown.

        @exception GymError The page did not load.
        """
        ...

    def list_my_bookings(self) -> list[BookingEntry]:
        """@brief Read every confirmed booking and waitlist entry of the My Bookings page.

        @return The entries, confirmed ones first; empty when the page shows its empty state.
        @exception GymError The page shows an error (the message is its text) or did not settle.
        """
        ...

    def save_text_screenshot(self, text: str, path: Path) -> None:
        """@brief Save an image of console text.

        @param text The lines to draw, in a dark monospace style.
        @param path The PNG file to write; its folders are created.
        """
        ...

    def save_screenshot(self, path: Path) -> None:
        """@brief Save a screenshot of the current page.

        @param path The PNG file to write; its folders are created.
        """
        ...

    def close(self) -> None:
        """@brief Close the browser."""
        ...
