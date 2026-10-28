"""@file constants.py
@brief Every constant of the bot: the site address, selectors, timings and messages.

Selectors of the gym pages are added here by the milestone that first uses them.
"""

from typing import Final

## Address of the Snack and Lift practice site on GitHub Pages (appbrewery/gym).
GYM_URL: Final[str] = "https://appbrewery.github.io/gym/"

## Folder, below the working directory, where Chrome keeps the profile of the bot.
PROFILE_DIR_NAME: Final[str] = "chrome_profile"

## Longest time to wait for an element of the page, in seconds.
WAIT_TIMEOUT_SECONDS: Final[int] = 10

## Attempts of the `retry` wrapper before it gives up (lecture step 9).
RETRY_COUNT: Final[int] = 7

## Weekdays of the classes the bot books, as the site abbreviates them.
TARGET_WEEKDAYS: Final[tuple[str, ...]] = ("Tue", "Thu")

## Id of the login button in the navigation bar of the site (the home page has no title).
NAV_LOGIN_BUTTON_ID: Final[str] = "login-button"

## Id of the e-mail field of the login form.
LOGIN_EMAIL_INPUT_ID: Final[str] = "email-input"

## Id of the password field of the login form.
LOGIN_PASSWORD_INPUT_ID: Final[str] = "password-input"

## Id of the submit button of the login form.
LOGIN_SUBMIT_BUTTON_ID: Final[str] = "submit-button"

## Id of the element that shows a login error.
ERROR_MESSAGE_ID: Final[str] = "error-message"

## Id of the class schedule page, shown after a successful login.
SCHEDULE_PAGE_ID: Final[str] = "schedule-page"

## Name of the environment variable that holds the account e-mail.
ACCOUNT_EMAIL_ENV: Final[str] = "SNACK_AND_LIFT_EMAIL"

## Name of the environment variable that holds the account password.
ACCOUNT_PASSWORD_ENV: Final[str] = "SNACK_AND_LIFT_PASSWORD"

## Folder where screenshots of a container run are written.
SCREENSHOT_DIR: Final[str] = "docs/images"

## Name of the environment variable that holds the path of the browser binary.
CHROME_BIN_ENV: Final[str] = "CHROME_BIN"

## Name of the environment variable that holds the path of the browser driver.
CHROMEDRIVER_PATH_ENV: Final[str] = "CHROMEDRIVER_PATH"

## Window size of the browser, so screenshots look the same on every machine.
WINDOW_SIZE: Final[str] = "1280,1600"

## Chromium arguments that a container needs to run without a display.
HEADLESS_BROWSER_ARGUMENTS: Final[tuple[str, ...]] = (
    "--headless=new",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
)
