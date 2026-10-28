"""@file test_cli.py
@brief The command line accepts its options and the entry point returns 0.
"""

from snack_and_lift.cli import main, parse_args


def test_headless_is_off_by_default() -> None:
    assert parse_args([]).headless is False


def test_headless_flag_is_read() -> None:
    assert parse_args(["--headless"]).headless is True


def test_main_returns_zero() -> None:
    assert main([]) == 0
