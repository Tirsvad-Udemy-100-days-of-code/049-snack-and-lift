"""@file test_date_independence.py
@brief The bot picks classes by weekday and time only, whatever the first visible day is.
"""

from datetime import date, timedelta

import pytest
from tests.unit.fakes import FakeGym

from snack_and_lift.application.booking import book_target_classes
from snack_and_lift.application.verification import verify_bookings
from snack_and_lift.domain.models import ClassCard
from snack_and_lift.domain.rules import find_target_classes

## A Monday; the schedules below start on this day plus an offset, so every weekday occurs.
_A_MONDAY = date(2025, 8, 11)
_DAYS_SHOWN = 8
_TUESDAY, _THURSDAY = 1, 3
_TIMES = (
    ("Time: 6:00 AM", "Book Class"),
    ("Time: 6:00 PM", "Book Class"),
    ("Time: 7:00 PM", "Book Class"),
)


def _day_text(day: date) -> str:
    return f"{day:%a}, {day:%b} {day.day}"


def _label(index: int, day: date) -> str:
    if index == 0:
        return f"Today ({_day_text(day)})"
    if index == 1:
        return f"Tomorrow ({_day_text(day)})"
    return _day_text(day)


def make_schedule(start_offset: int) -> tuple[list[ClassCard], set[str]]:
    """@brief Cards of 8 days from a start weekday, and the ids of the Tue/Thu 6pm ones."""
    cards: list[ClassCard] = []
    wanted: set[str] = set()
    for index in range(_DAYS_SHOWN):
        day = _A_MONDAY + timedelta(days=start_offset + index)
        for slot, (time_text, button) in enumerate(_TIMES):
            card_id = f"{index}{slot}"
            cards.append(ClassCard(card_id, "Spin Class", _label(index, day), time_text, button))
            if day.weekday() in (_TUESDAY, _THURSDAY) and slot == 1:
                wanted.add(card_id)
    return cards, wanted


@pytest.mark.parametrize("start_offset", range(7))
def test_find_target_classes_for_every_starting_weekday(start_offset: int) -> None:
    cards, wanted = make_schedule(start_offset)

    assert {card.card_id for card in find_target_classes(cards)} == wanted
    assert wanted


@pytest.mark.parametrize("start_offset", range(7))
def test_booking_and_verification_for_every_starting_weekday(start_offset: int) -> None:
    cards, wanted = make_schedule(start_offset)
    gym = FakeGym(cards=cards)

    results = book_target_classes(gym)

    assert set(gym.pressed) == wanted
    assert len(gym.pressed) == len(wanted)
    assert verify_bookings(gym, results).is_success


def test_schedule_whose_first_visible_day_is_a_thursday_includes_today() -> None:
    cards, _ = make_schedule(3)
    assert cards[0].day_label.startswith("Today (Thu,")

    chosen = find_target_classes(cards)

    assert [card.weekday for card in chosen] == ["Thu", "Tue", "Thu"]
    assert chosen[0].card_id == "01"


def test_card_order_does_not_change_which_classes_are_chosen() -> None:
    cards, wanted = make_schedule(2)

    chosen = find_target_classes(list(reversed(cards)))

    assert {card.card_id for card in chosen} == wanted
