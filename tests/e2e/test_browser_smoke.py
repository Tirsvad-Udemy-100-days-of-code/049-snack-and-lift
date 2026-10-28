"""@file test_browser_smoke.py
@brief Real-browser smoke test; runs only in the Docker container (SNACK_AND_LIFT_E2E=1).
"""

import os
import tempfile
from pathlib import Path

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from snack_and_lift import constants
from snack_and_lift.infrastructure.browser import create_driver

pytestmark = [
    pytest.mark.browser,
    pytest.mark.skipif(
        os.environ.get("SNACK_AND_LIFT_E2E") != "1",
        reason="needs a real browser; run it in the Docker container",
    ),
]


def test_gym_home_page_shows_the_login_button() -> None:
    driver = create_driver(headless=True, profile_dir=Path(tempfile.mkdtemp()), keep_open=False)
    try:
        driver.get(constants.GYM_URL)
        button = WebDriverWait(driver, constants.WAIT_TIMEOUT_SECONDS).until(
            ec.presence_of_element_located((By.ID, constants.NAV_LOGIN_BUTTON_ID))
        )
        assert button.text == "Login"
    finally:
        driver.quit()
