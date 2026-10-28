"""@file fakes.py
@brief A fake of the GymPort for the unit tests.
"""

from pathlib import Path

from snack_and_lift.domain.errors import LoginFailedError


class FakeGym:
    """@brief Records the calls; can be told to refuse the login."""

    def __init__(self, login_error: str | None = None) -> None:
        self.login_error = login_error
        self.calls: list[str] = []
        self.logins: list[tuple[str, str]] = []
        self.screenshots: list[Path] = []
        self.closed = False

    def open_site(self) -> None:
        self.calls.append("open_site")

    def log_in(self, email: str, password: str) -> None:
        self.calls.append("log_in")
        self.logins.append((email, password))
        if self.login_error is not None:
            raise LoginFailedError(self.login_error)

    def save_screenshot(self, path: Path) -> None:
        self.calls.append("save_screenshot")
        self.screenshots.append(path)

    def close(self) -> None:
        self.calls.append("close")
        self.closed = True
