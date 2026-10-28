"""@file test_selenium_gym.py
@brief The Selenium adapter against local HTML fixtures; runs only in the Docker container.
"""

import os
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from snack_and_lift.application.booking import book_target_classes
from snack_and_lift.application.verification import get_my_bookings
from snack_and_lift.domain.booking_entry import BookingEntry
from snack_and_lift.domain.errors import GymError, LoginFailedError, NoBookingsFoundError
from snack_and_lift.domain.models import Outcome
from snack_and_lift.infrastructure.browser import create_driver
from snack_and_lift.infrastructure.selenium_gym import SeleniumGym

pytestmark = [
    pytest.mark.browser,
    pytest.mark.skipif(
        os.environ.get("SNACK_AND_LIFT_E2E") != "1",
        reason="needs a real browser; run it in the Docker container",
    ),
]

FIXTURE_HOME = (Path(__file__).parent / "fixtures" / "home.html").as_uri()
# Dummy account that the fixture login.html accepts; it is not a real account.
FIXTURE_EMAIL = "fixture@example.invalid"
FIXTURE_PASSWORD = "fixture-password"


@pytest.fixture
def gym(tmp_path: Path) -> Iterator[SeleniumGym]:
    driver = create_driver(headless=True, profile_dir=tmp_path / "profile", keep_open=False)
    try:
        yield SeleniumGym(driver, base_url=FIXTURE_HOME)
    finally:
        driver.quit()


def test_log_in_succeeds_with_accepted_credentials(gym: SeleniumGym) -> None:
    gym.open_site()

    gym.log_in(FIXTURE_EMAIL, FIXTURE_PASSWORD)


def test_log_in_raises_for_wrong_credentials(gym: SeleniumGym) -> None:
    gym.open_site()

    with pytest.raises(LoginFailedError, match="Invalid"):
        gym.log_in(FIXTURE_EMAIL, "wrong-password")


def test_save_screenshot_creates_the_folder(gym: SeleniumGym, tmp_path: Path) -> None:
    gym.open_site()
    target = tmp_path / "shots" / "step-1.png"

    gym.save_screenshot(target)

    assert target.stat().st_size > 0


FIXTURE_SCHEDULE = (Path(__file__).parent / "fixtures" / "schedule.html").as_uri()


@pytest.fixture
def schedule_gym(tmp_path: Path) -> Iterator[SeleniumGym]:
    driver = create_driver(headless=True, profile_dir=tmp_path / "profile", keep_open=False)
    try:
        driver.get(FIXTURE_SCHEDULE)
        yield SeleniumGym(driver, base_url=FIXTURE_SCHEDULE)
    finally:
        driver.quit()


def test_list_class_cards_reads_the_day_from_the_ancestor_group(schedule_gym: SeleniumGym) -> None:
    cards = {card.card_id: card for card in schedule_gym.list_class_cards()}

    assert list(cards) == ["101", "102", "201", "401", "301", "302"]
    assert cards["102"].day_label == "Today (Wed, Aug 13)"
    assert cards["201"].weekday == "Thu"
    assert cards["302"].weekday == "Tue"
    assert cards["302"].name == "Spin Class"
    assert cards["302"].time_text == "Time: 6:00 PM"
    assert cards["302"].button_text == "Book Class"
    assert cards["101"].button_text == "Completed"
    assert cards["401"].button_text == "Booked"


def test_press_class_button_confirms_booking(schedule_gym: SeleniumGym) -> None:
    assert schedule_gym.press_class_button("102") == "Booked"


def test_press_class_button_confirms_waitlist(schedule_gym: SeleniumGym) -> None:
    assert schedule_gym.press_class_button("201") == "Waitlisted"


def test_press_class_button_raises_with_the_error_text_then_succeeds(
    schedule_gym: SeleniumGym,
) -> None:
    with pytest.raises(GymError, match="Network error"):
        schedule_gym.press_class_button("302")

    assert schedule_gym.press_class_button("302") == "Booked"


def test_save_text_screenshot_writes_a_png_and_keeps_the_page(
    schedule_gym: SeleniumGym, tmp_path: Path
) -> None:
    target = tmp_path / "shots" / "step-4.png"

    schedule_gym.save_text_screenshot("✓ Successfully booked: <Spin Class>", target)

    assert target.read_bytes().startswith(b"\x89PNG")
    assert schedule_gym.list_class_cards()


def test_book_target_classes_books_every_tuesday_and_thursday_class(
    schedule_gym: SeleniumGym,
) -> None:
    with pytest.raises(GymError, match="Network error"):
        book_target_classes(schedule_gym)

    results = book_target_classes(schedule_gym)

    assert [(r.card.card_id, r.outcome) for r in results] == [
        ("201", Outcome.ALREADY_WAITLISTED),
        ("302", Outcome.NEW_BOOKING),
    ]


FIXTURE_MY_BOOKINGS = (Path(__file__).parent / "fixtures" / "my_bookings.html").as_uri()


@pytest.fixture
def open_my_bookings_page(tmp_path: Path) -> Iterator[Callable[[str], SeleniumGym]]:
    """@brief Opens the My Bookings fixture in the given state (a query such as `?state=empty`)."""
    driver = create_driver(headless=True, profile_dir=tmp_path / "profile", keep_open=False)

    def open_page(query: str = "") -> SeleniumGym:
        driver.get(FIXTURE_MY_BOOKINGS + query)
        return SeleniumGym(driver, base_url=FIXTURE_MY_BOOKINGS)

    try:
        yield open_page
    finally:
        driver.quit()


def test_open_my_bookings_follows_the_nav_link(schedule_gym: SeleniumGym) -> None:
    schedule_gym.open_my_bookings()

    assert [entry.name for entry in schedule_gym.list_my_bookings()] == [
        "Spin Class",
        "Yoga Class",
        "HIIT Class",
    ]


def test_list_my_bookings_reads_confirmed_and_waitlist_entries(
    open_my_bookings_page: Callable[[str], SeleniumGym],
) -> None:
    entries = open_my_bookings_page("").list_my_bookings()

    assert entries == [
        BookingEntry("Spin Class", "Tue, Aug 12, 6:00 PM", False),
        BookingEntry("Yoga Class", "Wed, Aug 13, 7:00 AM", False),
        BookingEntry("HIIT Class", "Thu, Aug 14, 6:00 PM", True),
    ]


def test_list_my_bookings_returns_nothing_for_the_empty_state(
    open_my_bookings_page: Callable[[str], SeleniumGym],
) -> None:
    assert open_my_bookings_page("?state=empty").list_my_bookings() == []


def test_get_my_bookings_raises_for_the_empty_state(
    open_my_bookings_page: Callable[[str], SeleniumGym],
) -> None:
    with pytest.raises(NoBookingsFoundError):
        get_my_bookings(open_my_bookings_page("?state=empty"))


def test_list_my_bookings_raises_with_the_text_of_the_error_box(
    open_my_bookings_page: Callable[[str], SeleniumGym],
) -> None:
    with pytest.raises(GymError, match="Failed to load bookings"):
        open_my_bookings_page("?state=error").list_my_bookings()
