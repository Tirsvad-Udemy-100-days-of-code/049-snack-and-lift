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

## Weekday of the class that lecture steps 3 and 4 book, as the site abbreviates it.
NEXT_CLASS_WEEKDAY: Final[str] = "Tue"

## Hour (24-hour clock) of the class the bot books.
TARGET_HOUR: Final[int] = 18

## Minute of the class the bot books.
TARGET_MINUTE: Final[int] = 0

## CSS selector of every class card on the schedule.
CLASS_CARD_CSS: Final[str] = "div[id^='class-card-']"

## Prefix of the element ids of one card; the card id (for example "123") follows it.
CLASS_CARD_ID_PREFIX: Final[str] = "class-card-"
CLASS_NAME_ID_PREFIX: Final[str] = "class-name-"
CLASS_TIME_ID_PREFIX: Final[str] = "class-time-"
BOOK_BUTTON_ID_PREFIX: Final[str] = "book-button-"
COMPLETED_LABEL_ID_PREFIX: Final[str] = "completed-label-"
CLASS_ERROR_ID_PREFIX: Final[str] = "class-error-"

## XPath, relative to a card, of the title of the day group the card is in (the "ancestor" hint).
DAY_TITLE_XPATH: Final[str] = (
    "ancestor::div[starts-with(@id,'day-group-')]//h2[starts-with(@id,'day-title-')]"
)

## Texts of the button of a card.
BUTTON_TEXT_BOOK: Final[str] = "Book Class"
BUTTON_TEXT_JOIN_WAITLIST: Final[str] = "Join Waitlist"
BUTTON_TEXT_BOOKED: Final[str] = "Booked"
BUTTON_TEXT_WAITLISTED: Final[str] = "Waitlisted"
BUTTON_TEXT_BOOKING: Final[str] = "Booking..."
BUTTON_TEXT_JOINING: Final[str] = "Joining..."
BUTTON_TEXT_COMPLETED: Final[str] = "Completed"

## Prefix of the time text of a card ("Time: 6:00 PM").
TIME_TEXT_PREFIX: Final[str] = "Time:"

## Day labels the site wraps around the date of the next two days.
DAY_LABEL_WRAPPERS: Final[tuple[str, ...]] = ("Today", "Tomorrow")

## Console messages of the booking, with the class name and the day label as the site shows it.
MESSAGE_BOOKED: Final[str] = "✓ Successfully booked: {name} on {day}"
MESSAGE_WAITLISTED: Final[str] = "✓ Joined waitlist for: {name} on {day}"
MESSAGE_ALREADY_BOOKED: Final[str] = "✓ Already booked: {name} on {day}"
MESSAGE_ALREADY_WAITLISTED: Final[str] = "✓ Already on waitlist: {name} on {day}"
MESSAGE_NO_CLASS_FOUND: Final[str] = "No {weekday} class at {time} found on the schedule"

## File names of the screenshots of lecture steps 3 and 4.
SCREENSHOT_STEP_3: Final[str] = "step-3.png"
SCREENSHOT_STEP_4: Final[str] = "step-4.png"

## `string.Template` of the page that renders console text for a screenshot.
CONSOLE_PAGE_TEMPLATE: Final[str] = (
    "<!DOCTYPE html><html><head><meta charset='utf-8'></head>"
    "<body style='margin:0;background:#1e1e1e;color:#d4d4d4'>"
    "<pre style='margin:0;padding:16px;font:16px/1.5 monospace;white-space:pre-wrap'>"
    "$text</pre></body></html>"
)

## Prefix of the `data:` URL that carries the console page.
CONSOLE_PAGE_URL_PREFIX: Final[str] = "data:text/html;charset=utf-8,"
