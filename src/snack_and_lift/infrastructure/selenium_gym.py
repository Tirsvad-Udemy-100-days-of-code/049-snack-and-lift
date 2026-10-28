"""@file selenium_gym.py
@brief The Selenium adapter of the GymPort.
"""

import functools
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Concatenate

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from snack_and_lift import constants
from snack_and_lift.domain.errors import GymError, LoginFailedError

logger = logging.getLogger(__name__)

_SELENIUM_ERRORS = (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)


def _translate_errors[S, **P, R](
    method: Callable[Concatenate[S, P], R],
) -> Callable[Concatenate[S, P], R]:
    """@brief Turn Selenium errors of a method into GymError.

    @param method The adapter method to wrap.
    @return The wrapped method.
    """

    @functools.wraps(method)
    def wrapper(self: S, *args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return method(self, *args, **kwargs)
        except _SELENIUM_ERRORS as error:
            raise GymError(f"{method.__name__} failed: {type(error).__name__}") from error

    return wrapper


class SeleniumGym:
    """@brief The gym site driven by a Selenium WebDriver."""

    def __init__(self, driver: WebDriver, base_url: str = constants.GYM_URL) -> None:
        """@brief Wrap a driver.

        @param driver A running WebDriver.
        @param base_url The address of the home page.
        """
        self._driver = driver
        self._base_url = base_url
        self._wait = WebDriverWait(driver, constants.WAIT_TIMEOUT_SECONDS)

    @_translate_errors
    def open_site(self) -> None:
        """@brief Open the home page and wait for the login button.

        @exception GymError The page did not load.
        """
        self._driver.get(self._base_url)
        self._wait.until(ec.presence_of_element_located((By.ID, constants.NAV_LOGIN_BUTTON_ID)))

    @_translate_errors
    def log_in(self, email: str, password: str) -> None:
        """@brief Fill in the login form and wait for the schedule or an error.

        @param email The account e-mail.
        @param password The account password.
        @exception LoginFailedError The site shows a login error.
        @exception GymError The page did not behave as expected.
        """
        self._wait.until(ec.element_to_be_clickable((By.ID, constants.NAV_LOGIN_BUTTON_ID))).click()
        self._wait.until(
            ec.presence_of_element_located((By.ID, constants.LOGIN_EMAIL_INPUT_ID))
        ).send_keys(email)
        self._driver.find_element(By.ID, constants.LOGIN_PASSWORD_INPUT_ID).send_keys(password)
        self._driver.find_element(By.ID, constants.LOGIN_SUBMIT_BUTTON_ID).click()
        self._wait.until(
            ec.any_of(
                ec.presence_of_element_located((By.ID, constants.SCHEDULE_PAGE_ID)),
                ec.presence_of_element_located((By.ID, constants.ERROR_MESSAGE_ID)),
            )
        )
        errors = self._driver.find_elements(By.ID, constants.ERROR_MESSAGE_ID)
        if errors:
            raise LoginFailedError(errors[0].text)

    def save_screenshot(self, path: Path) -> None:
        """@brief Save a screenshot of the current page.

        @param path The PNG file to write; its folders are created.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        self._driver.save_screenshot(str(path))

    def close(self) -> None:
        """@brief Quit the browser."""
        self._driver.quit()
