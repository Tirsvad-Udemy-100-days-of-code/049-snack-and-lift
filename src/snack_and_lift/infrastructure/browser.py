"""@file browser.py
@brief Creates the Chrome driver with a persistent profile, headless when asked.
"""

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from snack_and_lift import constants


def default_profile_dir() -> Path:
    """@brief The folder where Chrome keeps the profile of the bot.

    @return `chrome_profile` below the working directory.
    """
    return Path.cwd() / constants.PROFILE_DIR_NAME


def build_options(headless: bool, profile_dir: Path, keep_open: bool) -> Options:
    """@brief Build the Chrome options (no browser is started).

    @param headless True to run without a window, as in the Docker container.
    @param profile_dir The Chrome user data folder.
    @param keep_open True to leave the browser open when the program ends.
    @return The options.
    """
    options = Options()
    options.add_argument(f"--user-data-dir={profile_dir}")
    options.add_argument(f"--window-size={constants.WINDOW_SIZE}")
    if keep_open:
        options.add_experimental_option("detach", True)
    if headless:
        for argument in constants.HEADLESS_BROWSER_ARGUMENTS:
            options.add_argument(argument)
    binary = os.environ.get(constants.CHROME_BIN_ENV)
    if binary:
        options.binary_location = binary
    return options


def create_driver(headless: bool, profile_dir: Path, keep_open: bool) -> webdriver.Chrome:
    """@brief Start Chrome.

    The binary and the driver come from `CHROME_BIN` and `CHROMEDRIVER_PATH` when
    these are set (the Docker image sets them); otherwise Selenium finds them.

    @param headless True to run without a window, as in the Docker container.
    @param profile_dir The Chrome user data folder; it is created when missing.
    @param keep_open True to leave the browser open when the program ends.
    @return A running Chrome driver.
    """
    profile_dir.mkdir(parents=True, exist_ok=True)
    options = build_options(headless, profile_dir, keep_open)
    driver_path = os.environ.get(constants.CHROMEDRIVER_PATH_ENV)
    service = Service(executable_path=driver_path) if driver_path else Service()
    return webdriver.Chrome(service=service, options=options)
