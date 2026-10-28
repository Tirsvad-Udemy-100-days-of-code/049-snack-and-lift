"""@file test_cli.py
@brief The command line accepts its options and the entry point wires the use case.
"""

from pathlib import Path

import pytest
from tests.unit.fakes import FakeGym
from tests.unit.test_models import make_card

from snack_and_lift import constants
from snack_and_lift.cli import main, parse_args
from snack_and_lift.infrastructure.browser import default_profile_dir

DUMMY_EMAIL = "dummy@example.invalid"
DUMMY_PASSWORD = "dummy-password"


@pytest.fixture
def credentials_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(constants.ACCOUNT_EMAIL_ENV, DUMMY_EMAIL)
    monkeypatch.setenv(constants.ACCOUNT_PASSWORD_ENV, DUMMY_PASSWORD)


def test_headless_is_off_by_default() -> None:
    assert parse_args([]).headless is False


def test_headless_flag_is_read() -> None:
    assert parse_args(["--headless"]).headless is True


def test_browser_stays_open_by_default_when_not_headless() -> None:
    assert parse_args([]).keep_open is True


def test_browser_is_closed_by_default_when_headless() -> None:
    assert parse_args(["--headless"]).keep_open is False


def test_keep_open_flag_overrides_headless_default() -> None:
    assert parse_args(["--headless", "--keep-open"]).keep_open is True


def test_profile_dir_defaults_to_working_directory() -> None:
    assert parse_args([]).profile_dir == default_profile_dir()


def test_profile_dir_option_is_read(tmp_path: Path) -> None:
    assert parse_args(["--profile-dir", str(tmp_path)]).profile_dir == tmp_path


def test_screenshot_dir_is_optional() -> None:
    assert parse_args([]).screenshot_dir is None


@pytest.mark.usefixtures("credentials_env")
def test_main_saves_both_screenshots_on_success(tmp_path: Path) -> None:
    gym = FakeGym()

    code = main(["--screenshot-dir", str(tmp_path)], lambda *_: gym)

    assert code == 0
    assert gym.logins == [(DUMMY_EMAIL, DUMMY_PASSWORD)]
    assert gym.screenshots == [
        tmp_path / "step-1.png",
        tmp_path / "step-2.png",
        tmp_path / "step-3.png",
    ]
    assert [path for _, path in gym.text_screenshots] == [tmp_path / "step-4.png"]
    assert gym.calls == [
        "open_site",
        "save_screenshot",
        "log_in",
        "save_screenshot",
        "list_class_cards",
        "save_screenshot",
        "save_text_screenshot",
    ]


@pytest.mark.usefixtures("credentials_env")
def test_main_books_the_class_and_draws_the_console_text(tmp_path: Path) -> None:
    gym = FakeGym(cards=[make_card("Tue, Aug 19")])

    assert main(["--screenshot-dir", str(tmp_path)], lambda *_: gym) == 0

    assert gym.pressed == ["123"]
    text, _ = gym.text_screenshots[0]
    assert "✓ Logged in" in text
    assert "✓ Successfully booked: Spin Class on Tue, Aug 19" in text


@pytest.mark.usefixtures("credentials_env")
def test_main_returns_1_when_the_booking_fails() -> None:
    gym = FakeGym(cards=[make_card("Tue, Aug 19")], press_error="Network down")

    assert main(["--headless"], lambda *_: gym) == 1
    assert gym.closed is True


@pytest.mark.usefixtures("credentials_env")
def test_main_saves_no_screenshot_without_directory() -> None:
    gym = FakeGym()

    assert main([], lambda *_: gym) == 0
    assert gym.screenshots == []


def test_main_returns_2_when_credentials_are_missing(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.delenv(constants.ACCOUNT_EMAIL_ENV, raising=False)
    monkeypatch.delenv(constants.ACCOUNT_PASSWORD_ENV, raising=False)
    gym = FakeGym()

    code = main([], lambda *_: gym)

    assert code == 2
    assert gym.calls == []
    assert constants.ACCOUNT_EMAIL_ENV in caplog.text


@pytest.mark.usefixtures("credentials_env")
def test_main_returns_1_when_login_fails() -> None:
    gym = FakeGym(login_error="Invalid credentials")

    assert main(["--headless"], lambda *_: gym) == 1
    assert gym.closed is True


@pytest.mark.usefixtures("credentials_env")
def test_main_closes_the_gym_when_not_kept_open() -> None:
    gym = FakeGym()

    assert main(["--headless"], lambda *_: gym) == 0
    assert gym.closed is True


@pytest.mark.usefixtures("credentials_env")
def test_main_keeps_the_gym_open_when_asked() -> None:
    gym = FakeGym()

    assert main([], lambda *_: gym) == 0
    assert gym.closed is False


@pytest.mark.usefixtures("credentials_env")
def test_main_passes_options_to_the_factory(tmp_path: Path) -> None:
    received: list[tuple[bool, Path, bool]] = []

    def factory(headless: bool, profile_dir: Path, keep_open: bool) -> FakeGym:
        received.append((headless, profile_dir, keep_open))
        return FakeGym()

    main(["--headless", "--profile-dir", str(tmp_path)], factory)

    assert received == [(True, tmp_path, False)]
