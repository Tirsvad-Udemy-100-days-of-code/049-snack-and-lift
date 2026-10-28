"""@file test_browser_options.py
@brief The Chrome options are built correctly (no browser is started).
"""

from pathlib import Path

import pytest

from snack_and_lift import constants
from snack_and_lift.infrastructure.browser import build_options, default_profile_dir


def test_profile_dir_is_passed_to_chrome(tmp_path: Path) -> None:
    options = build_options(False, tmp_path, False)

    assert f"--user-data-dir={tmp_path}" in options.arguments


def test_default_profile_dir_is_below_the_working_directory() -> None:
    assert default_profile_dir() == Path.cwd() / constants.PROFILE_DIR_NAME


def test_keep_open_detaches_the_browser(tmp_path: Path) -> None:
    assert build_options(False, tmp_path, True).experimental_options["detach"] is True


def test_browser_is_not_detached_when_not_kept_open(tmp_path: Path) -> None:
    assert "detach" not in build_options(False, tmp_path, False).experimental_options


def test_headless_adds_the_headless_arguments(tmp_path: Path) -> None:
    options = build_options(True, tmp_path, False)

    for argument in constants.HEADLESS_BROWSER_ARGUMENTS:
        assert argument in options.arguments


def test_window_has_no_headless_arguments_by_default(tmp_path: Path) -> None:
    options = build_options(False, tmp_path, False)

    assert "--headless=new" not in options.arguments
    assert f"--window-size={constants.WINDOW_SIZE}" in options.arguments


def test_chrome_binary_comes_from_the_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv(constants.CHROME_BIN_ENV, "/opt/chrome")

    assert build_options(False, tmp_path, False).binary_location == "/opt/chrome"
