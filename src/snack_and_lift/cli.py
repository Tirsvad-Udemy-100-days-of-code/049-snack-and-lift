"""@file cli.py
@brief Command-line entry point (the composition root of the bot).
"""

import argparse
import logging
import os
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

from snack_and_lift.application.credentials import load_credentials
from snack_and_lift.application.ports import GymPort
from snack_and_lift.application.session import login
from snack_and_lift.domain.errors import LoginFailedError, MissingCredentialsError
from snack_and_lift.infrastructure.browser import create_driver, default_profile_dir
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


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """@brief Read the command line.

    @param argv Arguments without the program name; None reads `sys.argv`.
    @return The parsed options; `keep_open` is True unless `--headless` is given.
    """
    parser = argparse.ArgumentParser(
        prog="snack-and-lift",
        description="Books the Tuesday and Thursday 6pm classes at the Snack and Lift gym.",
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


def main(
    argv: Sequence[str] | None = None,
    gym_factory: GymFactory = selenium_gym_factory,
) -> int:
    """@brief Start the bot: open the site and log in.

    @param argv Arguments without the program name; None reads `sys.argv`.
    @param gym_factory Builds the gym site; tests pass a fake.
    @return Process exit code: 0 done, 1 login failed, 2 credentials missing.
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    _use_utf8_output()
    args = parse_args(argv)
    try:
        credentials = load_credentials(os.environ)
    except MissingCredentialsError as error:
        logger.error("%s", error)
        return 2
    gym = gym_factory(args.headless, args.profile_dir, args.keep_open)
    try:
        gym.open_site()
        _save_step(gym, args.screenshot_dir, "step-1.png")
        login(gym, credentials)
        _save_step(gym, args.screenshot_dir, "step-2.png")
    except LoginFailedError as error:
        logger.error("Login failed: %s", error)
        return 1
    finally:
        if not args.keep_open:
            gym.close()
    return 0
