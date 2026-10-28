"""@file cli.py
@brief Command-line entry point (the composition root of the bot).
"""

import argparse
import logging
from collections.abc import Sequence

logger = logging.getLogger(__name__)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """@brief Read the command line.

    @param argv Arguments without the program name; None reads `sys.argv`.
    @return The parsed options.
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
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """@brief Start the bot.

    @param argv Arguments without the program name; None reads `sys.argv`.
    @return Process exit code.
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parse_args(argv)
    logger.info("snack-and-lift: the lecture steps are added by the next milestones")
    return 0
