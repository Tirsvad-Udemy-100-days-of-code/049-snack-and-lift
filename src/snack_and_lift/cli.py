"""@file cli.py
@brief Command-line entry point (the composition root of the bot).
"""

import argparse
import logging
import os
import sys
import time
from collections.abc import Callable, Sequence
from pathlib import Path

from snack_and_lift import constants
from snack_and_lift.application.booking import book_next_tuesday, book_target_classes
from snack_and_lift.application.credentials import (
    Credentials,
    load_admin_credentials,
    load_credentials,
)
from snack_and_lift.application.ports import GymPort
from snack_and_lift.application.retry import Sleep
from snack_and_lift.application.session import login_with_retry
from snack_and_lift.application.verification import verify_bookings
from snack_and_lift.domain.errors import GymError, LoginFailedError, MissingCredentialsError
from snack_and_lift.domain.models import ClassResult
from snack_and_lift.domain.report import format_detail_list, format_summary
from snack_and_lift.domain.verification import format_verification
from snack_and_lift.infrastructure.browser import create_driver, default_profile_dir
from snack_and_lift.infrastructure.console_recorder import ConsoleRecorder
from snack_and_lift.infrastructure.env_file import read_env_file
from snack_and_lift.infrastructure.selenium_gym import SeleniumGym

## Builds the gym site from (headless, profile folder, keep open).
GymFactory = Callable[[bool, Path, bool], GymPort]

logger = logging.getLogger(__name__)


def selenium_gym_factory(headless: bool, profile_dir: Path, keep_open: bool) -> GymPort:
    """@brief Start Chrome and wrap it as the gym site.

    @param headless True to run without a window.
    @param profile_dir The Chrome user data folder.
    @param keep_open True to leave the browser open when the program ends.
    @return The gym site.
    """
    return SeleniumGym(create_driver(headless, profile_dir, keep_open))


def _at_least_one(text: str) -> int:
    """@brief Read a whole number of at least 1 for an option.

    @param text The text of the option.
    @return The number.
    @exception argparse.ArgumentTypeError The text is not a whole number of at least 1.
    """
    try:
        number = int(text)
    except ValueError:
        number = 0
    if number < 1:
        raise argparse.ArgumentTypeError(f"{text!r} is not a whole number of at least 1")
    return number


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """@brief Read the command line.

    @param argv Arguments without the program name; None reads `sys.argv`.
    @return The parsed options; `keep_open` is True unless `--headless` is given.
    """
    parser = argparse.ArgumentParser(
        prog="snack-and-lift",
        description="Books the Tuesday and Thursday 6pm classes at the Snack and Lift gym.",
        epilog=(
            "exit codes: 0 done, 1 a step failed (also when every retry failed), "
            "2 credentials missing in the environment or the env file, "
            "3 the My Bookings page does not match the bookings made"
        ),
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="run Chrome without a window (the Docker image does this)",
    )
    parser.add_argument(
        "--keep-open",
        action="store_true",
        default=None,
        help="leave the browser open at the end (default when not headless)",
    )
    parser.add_argument(
        "--profile-dir",
        type=Path,
        default=None,
        help="Chrome profile folder (default: ./chrome_profile)",
    )
    parser.add_argument(
        "--screenshot-dir",
        type=Path,
        default=None,
        help="save a screenshot after each step into this folder",
    )
    parser.add_argument(
        "--first-tuesday-only",
        action="store_true",
        help="book only the next Tuesday 6pm class (lecture steps 3 and 4); skips the verification",
    )
    parser.add_argument(
        "--retries",
        type=_at_least_one,
        default=constants.RETRY_COUNT,
        metavar="N",
        help=(
            "attempts for the login, each booking and the My Bookings page when the site "
            f"drops a request (default: {constants.RETRY_COUNT}, at least 1)"
        ),
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=Path(constants.ENV_FILE_NAME),
        metavar="PATH",
        help=(
            "file with the gym accounts as KEY=VALUE lines "
            f"(default: ./{constants.ENV_FILE_NAME}); a real environment variable wins"
        ),
    )
    args = parser.parse_args(argv)
    if args.keep_open is None:
        args.keep_open = not args.headless
    if args.profile_dir is None:
        args.profile_dir = default_profile_dir()
    return args


def _use_utf8_output() -> None:
    """@brief Make stdout UTF-8 so the check mark of the messages prints on Windows."""
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(encoding="utf-8")


def _save_step(gym: GymPort, screenshot_dir: Path | None, name: str) -> None:
    """@brief Save a screenshot when a folder was asked for.

    @param gym The gym site.
    @param screenshot_dir The folder, or None for no screenshots.
    @param name The file name.
    """
    if screenshot_dir is not None:
        gym.save_screenshot(screenshot_dir / name)


def _save_console(gym: GymPort, screenshot_dir: Path | None, text: str, name: str) -> None:
    """@brief Save console text as an image when a folder was asked for.

    @param gym The gym site.
    @param screenshot_dir The folder, or None for no screenshots.
    @param text The console text to draw.
    @param name The file name.
    """
    if screenshot_dir is not None:
        gym.save_text_screenshot(text, screenshot_dir / name)


def _run(
    gym: GymPort,
    args: argparse.Namespace,
    recorder: ConsoleRecorder,
    credentials: Credentials,
    sleep: Sleep,
) -> bool:
    """@brief Open the site, log in, book the classes and verify them, saving the step images.

    Books every Tuesday and Thursday 6pm class, logs the summary and the detailed list and
    verifies the bookings on the My Bookings page; with `--first-tuesday-only` it books the
    next Tuesday class only and does not verify.

    @param gym The gym site.
    @param args The parsed options.
    @param recorder The recorded console lines, drawn for step 4.
    @param credentials The account to log in with.
    @param sleep Waits between two attempts of a retried step.
    @return False when the My Bookings page does not match the bookings made, else True.
    @exception GymError A step failed on every attempt.
    """
    gym.open_site()
    _save_step(gym, args.screenshot_dir, "step-1.png")
    login_with_retry(gym, credentials, args.retries, sleep)
    _save_step(gym, args.screenshot_dir, "step-2.png")
    if args.first_tuesday_only:
        book_next_tuesday(gym, args.retries, sleep)
        _save_step(gym, args.screenshot_dir, constants.SCREENSHOT_STEP_3)
        _save_console(gym, args.screenshot_dir, recorder.text, constants.SCREENSHOT_STEP_4)
        return True
    window_saved = False

    def save_window_once(_: ClassResult) -> None:
        nonlocal window_saved
        if not window_saved:
            _save_step(gym, args.screenshot_dir, constants.SCREENSHOT_STEP_3)
            window_saved = True

    results = book_target_classes(gym, save_window_once, args.retries, sleep)
    if not window_saved:
        _save_step(gym, args.screenshot_dir, constants.SCREENSHOT_STEP_3)
    _save_console(gym, args.screenshot_dir, recorder.text, constants.SCREENSHOT_STEP_4)
    summary = format_summary(results)
    logger.info("%s", summary)
    _save_console(gym, args.screenshot_dir, summary, constants.SCREENSHOT_STEP_5)
    detail = format_detail_list(results)
    logger.info("%s", detail)
    _save_console(gym, args.screenshot_dir, f"{summary}\n{detail}", constants.SCREENSHOT_STEP_6)
    verification = verify_bookings(gym, results, args.retries, sleep)
    _save_step(gym, args.screenshot_dir, constants.SCREENSHOT_STEP_7)
    verification_text = format_verification(verification)
    logger.info("%s", verification_text)
    _save_console(gym, args.screenshot_dir, verification_text, constants.SCREENSHOT_STEP_8)
    _save_console(gym, args.screenshot_dir, recorder.text, constants.SCREENSHOT_STEP_9)
    return verification.is_success


def main(
    argv: Sequence[str] | None = None,
    gym_factory: GymFactory = selenium_gym_factory,
    sleep: Sleep = time.sleep,
) -> int:
    """@brief Start the bot: open the site, log in, book the classes and verify them.

    @param argv Arguments without the program name; None reads `sys.argv`.
    @param gym_factory Builds the gym site; tests pass a fake.
    @param sleep Waits between two attempts of a retried step; tests pass a recorder.
    @return Process exit code: 0 done, 1 a step failed, 2 credentials missing, 3 mismatch.
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    recorder = ConsoleRecorder()
    root.addHandler(recorder)
    try:
        return _main(argv, gym_factory, recorder, sleep)
    finally:
        root.removeHandler(recorder)


def _main(
    argv: Sequence[str] | None, gym_factory: GymFactory, recorder: ConsoleRecorder, sleep: Sleep
) -> int:
    """@brief The body of `main`, run while the recorder is attached.

    @param argv Arguments without the program name.
    @param gym_factory Builds the gym site.
    @param recorder The console recorder.
    @param sleep Waits between two attempts of a retried step.
    @return Process exit code.
    """
    _use_utf8_output()
    args = parse_args(argv)
    try:
        environment = {**read_env_file(args.env_file), **os.environ}
        credentials = load_credentials(environment)
        load_admin_credentials(environment)  # load-only for now; nothing uses it yet
    except MissingCredentialsError as error:
        logger.error("%s", error)
        return 2
    gym = gym_factory(args.headless, args.profile_dir, args.keep_open)
    try:
        verified = _run(gym, args, recorder, credentials, sleep)
    except LoginFailedError as error:
        logger.error("Login failed: %s", error)
        return 1
    except GymError as error:
        logger.error("Failed: %s", error)
        return 1
    finally:
        if not args.keep_open:
            gym.close()
    return 0 if verified else constants.EXIT_VERIFICATION_MISMATCH
