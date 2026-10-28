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

## Seconds to wait between two attempts of the `retry` wrapper.
RETRY_DELAY_SECONDS: Final[float] = 0.5

## Name of a retried step that was given no description.
RETRY_DEFAULT_DESCRIPTION: Final[str] = "operation"

## Descriptions of the retried steps, as they appear in the log.
RETRY_DESCRIPTION_LOGIN: Final[str] = "login"
RETRY_DESCRIPTION_BOOK: Final[str] = "book {name} on {day}"
RETRY_DESCRIPTION_BOOKINGS: Final[str] = "get my bookings"

## Messages of the `retry` wrapper.
MESSAGE_RETRY_FAILED: Final[str] = (
    "⚠ Attempt {attempt}/{retries} failed: {description}: {error}. Retrying..."
)
MESSAGE_RETRY_SUCCEEDED: Final[str] = "✓ {description} succeeded after {attempts} attempts"
MESSAGE_RETRIES_EXHAUSTED: Final[str] = "{description} failed after {retries} attempts: {error}"
MESSAGE_RETRIES_INVALID: Final[str] = "retries must be at least 1, got {retries}"

## Error raised when a class card is no longer on the schedule while a booking is repeated.
MESSAGE_CLASS_NOT_ON_SCHEDULE: Final[str] = "class {card_id} not found on the schedule"

## File name of the screenshot of lecture step 9 (the console with the retry warnings).
SCREENSHOT_STEP_9: Final[str] = "step-9.png"

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

## Names of the environment variables that hold the admin account (read, not used yet).
ADMIN_EMAIL_ENV: Final[str] = "SNACK_AND_LIFT_ADMIN_EMAIL"
ADMIN_PASSWORD_ENV: Final[str] = "SNACK_AND_LIFT_ADMIN_PASSWORD"

## Error for an admin account with one variable only; {name} is the missing variable.
MESSAGE_ADMIN_HALF_SET: Final[str] = (
    "Set {name} too: the admin account needs both "
    "SNACK_AND_LIFT_ADMIN_EMAIL and SNACK_AND_LIFT_ADMIN_PASSWORD"
)

## Default file with the gym accounts, relative to the current directory.
ENV_FILE_NAME: Final[str] = ".env.gym"

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

## Logged when the schedule has no class on a target weekday at the target time.
MESSAGE_NO_TARGET_CLASSES: Final[str] = (
    "No Tuesday or Thursday class at {time} found on the schedule"
)

## Time of the target classes as written in messages (24-hour clock).
TARGET_TIME_TEXT: Final[str] = f"{TARGET_HOUR:02d}:{TARGET_MINUTE:02d}"

## Lines of the booking summary (lecture step 5).
SUMMARY_TITLE: Final[str] = "--- BOOKING SUMMARY ---"
SUMMARY_NEW_BOOKINGS: Final[str] = "New bookings: {count}"
SUMMARY_NEW_WAITLIST: Final[str] = "New waitlist entries: {count}"
SUMMARY_ALREADY_DONE: Final[str] = "Already booked/waitlisted: {count}"
SUMMARY_TOTAL: Final[str] = "Total Tuesday & Thursday 6pm classes: {count}"

## Lines of the detailed class list (lecture step 6).
DETAIL_TITLE: Final[str] = "--- DETAILED CLASS LIST ---"
DETAIL_LINE: Final[str] = "  • [{tag}] {name} on {day}"
DETAIL_NONE: Final[str] = "  No matching class found"
DETAIL_TAG_NEW_BOOKING: Final[str] = "New Booking"
DETAIL_TAG_NEW_WAITLIST: Final[str] = "New Waitlist"
DETAIL_TAG_ALREADY_BOOKED: Final[str] = "Already Booked"
DETAIL_TAG_ALREADY_WAITLISTED: Final[str] = "Already Waitlisted"

## File names of the screenshots of lecture steps 3 to 6.
SCREENSHOT_STEP_3: Final[str] = "step-3.png"
SCREENSHOT_STEP_4: Final[str] = "step-4.png"
SCREENSHOT_STEP_5: Final[str] = "step-5.png"
SCREENSHOT_STEP_6: Final[str] = "step-6.png"

## `string.Template` of the page that renders console text for a screenshot.
CONSOLE_PAGE_TEMPLATE: Final[str] = (
    "<!DOCTYPE html><html><head><meta charset='utf-8'></head>"
    "<body style='margin:0;background:#1e1e1e;color:#d4d4d4'>"
    "<pre style='margin:0;padding:16px;font:16px/1.5 monospace;white-space:pre-wrap'>"
    "$text</pre></body></html>"
)

## Prefix of the `data:` URL that carries the console page.
CONSOLE_PAGE_URL_PREFIX: Final[str] = "data:text/html;charset=utf-8,"

## File names of the screenshots of lecture steps 7 and 8.
SCREENSHOT_STEP_7: Final[str] = "step-7.png"
SCREENSHOT_STEP_8: Final[str] = "step-8.png"

## Process exit code when the My Bookings page does not match what the bot did.
EXIT_VERIFICATION_MISMATCH: Final[int] = 3

## Id of the navigation link that opens the My Bookings page.
MY_BOOKINGS_LINK_ID: Final[str] = "my-bookings-link"

## Id of the My Bookings page, shown after its bookings were loaded.
MY_BOOKINGS_PAGE_ID: Final[str] = "my-bookings-page"

## Id of the element shown when the account has no booking and no waitlist entry.
EMPTY_BOOKINGS_STATE_ID: Final[str] = "empty-bookings-state"

## CSS selectors of the confirmed booking cards and the waitlist cards.
BOOKING_CARD_CSS: Final[str] = "#confirmed-bookings-section div[id^='booking-card-']"
WAITLIST_CARD_CSS: Final[str] = "#waitlist-section div[id^='waitlist-card-']"

## Prefixes of the element ids of a booking card and of a waitlist card.
BOOKING_CARD_ID_PREFIX: Final[str] = "booking-card-"
BOOKING_NAME_ID_PREFIX: Final[str] = "booking-class-name-"
WAITLIST_CARD_ID_PREFIX: Final[str] = "waitlist-card-"
WAITLIST_NAME_ID_PREFIX: Final[str] = "waitlist-class-name-"

## XPath, relative to a card, of the paragraph "When: Tue, Aug 12, 6:00 PM".
WHEN_XPATH: Final[str] = ".//p[strong[starts-with(normalize-space(), 'When:')]]"

## Prefix of the date and time text of a booking card.
WHEN_TEXT_PREFIX: Final[str] = "When:"

## Suffix the My Bookings page adds to the name of a waitlist entry.
WAITLIST_NAME_SUFFIX: Final[str] = " (Waitlist)"

## Message of the error raised when the My Bookings page shows no booking at all.
MESSAGE_NO_BOOKINGS_FOUND: Final[str] = "The My Bookings page shows no booking or waitlist entry"

## Lines of the verification on the My Bookings page (lecture steps 7 and 8).
VERIFY_TITLE: Final[str] = "--- VERIFYING ON MY BOOKINGS PAGE ---"
VERIFY_LINE_VERIFIED: Final[str] = "  ✓ Verified: {name}"
VERIFY_RESULT_TITLE: Final[str] = "--- VERIFICATION RESULT ---"
VERIFY_EXPECTED: Final[str] = "Expected: {count} {noun}"
VERIFY_FOUND: Final[str] = "Found: {count} {noun}"
VERIFY_NOUN_SINGULAR: Final[str] = "booking"
VERIFY_NOUN_PLURAL: Final[str] = "bookings"
VERIFY_SUCCESS: Final[str] = "✅ SUCCESS: All bookings verified!"
VERIFY_MISMATCH: Final[str] = "❌ MISMATCH: Missing {count} bookings"
VERIFY_LINE_MISSING: Final[str] = "  ✗ Missing: {entry}"
VERIFY_LINE_UNEXPECTED: Final[str] = "  ? Unexpected: {entry}"
VERIFY_LINE_ALSO_BOOKED: Final[str] = "  i Also booked (not checked): {entry}"

## Month abbreviations of the dates on the pages, January first.
MONTH_ABBREVIATIONS: Final[tuple[str, ...]] = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)

## Days of a year, with the 29th of February, used to compare dates that have no year.
DAYS_IN_DATE_CYCLE: Final[int] = 366

## A leap year, so that the 29th of February is a valid date.
DATE_CYCLE_YEAR: Final[int] = 2000
