"""@file selenium_gym.py
@brief The Selenium adapter of the GymPort.
"""

import functools
import html
import logging
import urllib.parse
from collections.abc import Callable
from pathlib import Path
from string import Template
from typing import Concatenate, Literal

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from snack_and_lift import constants
from snack_and_lift.domain.errors import GymError, LoginFailedError
from snack_and_lift.domain.models import ButtonState, ClassCard

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

    @_translate_errors
    def list_class_cards(self) -> list[ClassCard]:
        """@brief Read every class card; the day comes from the ancestor day group.

        @return The classes in page order.
        @exception GymError The schedule could not be read.
        """
        self._wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, constants.CLASS_CARD_CSS))
        )
        elements = self._driver.find_elements(By.CSS_SELECTOR, constants.CLASS_CARD_CSS)
        return [self._read_card(element) for element in elements]

    def _read_card(self, element: WebElement) -> ClassCard:
        """@brief Turn one card element into plain data.

        @param element The card.
        @return The class.
        """
        card_id = (element.get_attribute("id") or "").removeprefix(constants.CLASS_CARD_ID_PREFIX)
        buttons = element.find_elements(By.ID, constants.BOOK_BUTTON_ID_PREFIX + card_id)
        labels = element.find_elements(By.ID, constants.COMPLETED_LABEL_ID_PREFIX + card_id)
        control = (buttons or labels or [None])[0]
        return ClassCard(
            card_id=card_id,
            name=element.find_element(By.ID, constants.CLASS_NAME_ID_PREFIX + card_id).text,
            day_label=element.find_element(By.XPATH, constants.DAY_TITLE_XPATH).text,
            time_text=element.find_element(By.ID, constants.CLASS_TIME_ID_PREFIX + card_id).text,
            button_text=control.text if control is not None else "",
        )

    @_translate_errors
    def press_class_button(self, card_id: str) -> str:
        """@brief Scroll to the button, click it and wait for the result or the error box.

        @param card_id The id of the card without its prefix.
        @return The new text of the button.
        @exception GymError The site shows an error for the class, or nothing settled in time.
        """
        button_id = constants.BOOK_BUTTON_ID_PREFIX + card_id
        button = self._wait.until(ec.presence_of_element_located((By.ID, button_id)))
        self._driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        before = button.text
        self._wait.until(ec.element_to_be_clickable((By.ID, button_id))).click()

        def settled(driver: WebDriver) -> tuple[str, str] | Literal[False]:
            errors = driver.find_elements(By.ID, constants.CLASS_ERROR_ID_PREFIX + card_id)
            text = driver.find_element(By.ID, button_id).text
            if errors:
                return text, errors[0].text or "class error"
            if text != before and ButtonState.from_text(text) is not ButtonState.BUSY:
                return text, ""
            return False

        text, error = self._wait.until(settled)
        if error:
            raise GymError(error)
        return text

    @_translate_errors
    def save_text_screenshot(self, text: str, path: Path) -> None:
        """@brief Draw console text in a temporary tab and save a screenshot of it.

        A tab is used so that the schedule page keeps its state.

        @param text The lines to draw.
        @param path The PNG file to write; its folders are created.
        """
        page = Template(constants.CONSOLE_PAGE_TEMPLATE).substitute(text=html.escape(text))
        original = self._driver.current_window_handle
        self._driver.switch_to.new_window("tab")
        try:
            self._driver.get(constants.CONSOLE_PAGE_URL_PREFIX + urllib.parse.quote(page))
            self.save_screenshot(path)
        finally:
            self._driver.close()
            self._driver.switch_to.window(original)

    def save_screenshot(self, path: Path) -> None:
        """@brief Save a screenshot of the current page.

        @param path The PNG file to write; its folders are created.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        self._driver.save_screenshot(str(path))

    def close(self) -> None:
        """@brief Quit the browser."""
        self._driver.quit()
