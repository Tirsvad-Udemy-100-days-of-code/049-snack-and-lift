"""@file test_selenium_gym.py
@brief The Selenium adapter against local HTML fixtures; runs only in the Docker container.
"""

import os
from collections.abc import Iterator
from pathlib import Path

import pytest

from snack_and_lift.domain.errors import LoginFailedError
from snack_and_lift.infrastructure.browser import create_driver
from snack_and_lift.infrastructure.selenium_gym import SeleniumGym

pytestmark = [
    pytest.mark.browser,
    pytest.mark.skipif(
        os.environ.get("SNACK_AND_LIFT_E2E") != "1",
        reason="needs a real browser; run it in the Docker container",
    ),
]

FIXTURE_HOME = (Path(__file__).parent / "fixtures" / "home.html").as_uri()
# Dummy account that the fixture login.html accepts; it is not a real account.
FIXTURE_EMAIL = "fixture@example.invalid"
FIXTURE_PASSWORD = "fixture-password"


@pytest.fixture
def gym(tmp_path: Path) -> Iterator[SeleniumGym]:
    driver = create_driver(headless=True, profile_dir=tmp_path / "profile", keep_open=False)
    try:
        yield SeleniumGym(driver, base_url=FIXTURE_HOME)
    finally:
        driver.quit()


def test_log_in_succeeds_with_accepted_credentials(gym: SeleniumGym) -> None:
    gym.open_site()

    gym.log_in(FIXTURE_EMAIL, FIXTURE_PASSWORD)


def test_log_in_raises_for_wrong_credentials(gym: SeleniumGym) -> None:
    gym.open_site()

    with pytest.raises(LoginFailedError, match="Invalid"):
        gym.log_in(FIXTURE_EMAIL, "wrong-password")


def test_save_screenshot_creates_the_folder(gym: SeleniumGym, tmp_path: Path) -> None:
    gym.open_site()
    target = tmp_path / "shots" / "step-1.png"

    gym.save_screenshot(target)

    assert target.stat().st_size > 0
