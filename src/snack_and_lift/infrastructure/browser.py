"""@file browser.py
@brief Creates the Chrome driver, headless when asked.
"""

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from snack_and_lift import constants


def create_driver(headless: bool) -> webdriver.Chrome:
    """@brief Start Chrome.

    The binary and the driver come from `CHROME_BIN` and `CHROMEDRIVER_PATH` when
    these are set (the Docker image sets them); otherwise Selenium finds them.

    @param headless True to run without a window, as in the Docker container.
    @return A running Chrome driver.
    """
    options = Options()
    options.add_argument(f"--window-size={constants.WINDOW_SIZE}")
    if headless:
        for argument in constants.HEADLESS_BROWSER_ARGUMENTS:
            options.add_argument(argument)
    binary = os.environ.get(constants.CHROME_BIN_ENV)
    if binary:
        options.binary_location = binary
    driver_path = os.environ.get(constants.CHROMEDRIVER_PATH_ENV)
    service = Service(executable_path=driver_path) if driver_path else Service()
    return webdriver.Chrome(service=service, options=options)
