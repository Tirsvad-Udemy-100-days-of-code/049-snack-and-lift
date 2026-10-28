"""@file ports.py
@brief The ports the use cases need from the outside world.
"""

from pathlib import Path
from typing import Protocol


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

    def save_screenshot(self, path: Path) -> None:
        """@brief Save a screenshot of the current page.

        @param path The PNG file to write; its folders are created.
        """
        ...

    def close(self) -> None:
        """@brief Close the browser."""
        ...
