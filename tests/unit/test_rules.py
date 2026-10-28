"""@file test_rules.py
@brief Day and time parsing, finding the target class, the decision and the messages.
"""

import pytest
from tests.unit.test_models import make_card

from snack_and_lift.domain.errors import PageFormatError, UnknownButtonError
from snack_and_lift.domain.models import Outcome
from snack_and_lift.domain.rules import (
    Action,
    decide_outcome_action,
    find_next_class,
    format_outcome,
    is_target_time,
    parse_day_label,
    parse_time,
)


@pytest.mark.parametrize(
    ("label", "expected"),
    [
        ("Today (Tue, Aug 12)", ("Tue", "Tue, Aug 12")),
        ("Tomorrow (Wed, Aug 13)", ("Wed", "Wed, Aug 13")),
        ("Thu, Aug 14", ("Thu", "Thu, Aug 14")),
        ("  Fri, Sep 5 ", ("Fri", "Fri, Sep 5")),
    ],
)
def test_day_label_is_split(label: str, expected: tuple[str, str]) -> None:
    assert parse_day_label(label) == expected


@pytest.mark.parametrize("label", ["", "Tuesday", "Today Tue, Aug 12", "Today (Tue, Aug 12", "x"])
def test_day_label_junk_raises(label: str) -> None:
    with pytest.raises(PageFormatError):
        parse_day_label(label)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("6:00 PM", (18, 0)),
        ("Time: 6:00 PM", (18, 0)),
        ("12:00 AM", (0, 0)),
        ("12:30 AM", (0, 30)),
        ("12:00 PM", (12, 0)),
        ("11:59 PM", (23, 59)),
        ("1:05 am", (1, 5)),
    ],
)
def test_time_is_read(text: str, expected: tuple[int, int]) -> None:
    assert parse_time(text) == expected


@pytest.mark.parametrize("text", ["", "noon", "6 PM", "0:00 AM", "13:00 PM", "6:60 PM", "18:00"])
def test_time_junk_raises(text: str) -> None:
    with pytest.raises(PageFormatError):
        parse_time(text)


def test_target_time_is_six_pm() -> None:
    assert is_target_time(make_card(time_text="Time: 6:00 PM"))
    assert not is_target_time(make_card(time_text="Time: 6:00 AM"))
    assert not is_target_time(make_card(time_text="Time: 6:30 PM"))


def test_next_class_is_found_when_the_schedule_starts_on_a_wednesday() -> None:
    cards = [
        make_card("Today (Wed, Aug 13)", card_id="1"),
        make_card("Thu, Aug 14", card_id="2"),
        make_card("Tue, Aug 19", time_text="Time: 7:00 AM", card_id="3"),
        make_card("Tue, Aug 19", card_id="4"),
        make_card("Tue, Aug 26", card_id="5"),
    ]

    found = find_next_class(cards, "Tue")

    assert found is not None
    assert found.card_id == "4"


def test_next_class_accepts_a_today_label() -> None:
    cards = [make_card("Today (Tue, Aug 12)", card_id="9")]

    found = find_next_class(cards, "Tue")

    assert found is not None
    assert found.card_id == "9"


def test_next_class_skips_completed_classes() -> None:
    cards = [
        make_card("Today (Tue, Aug 12)", button_text="Completed", card_id="1"),
        make_card("Tue, Aug 19", card_id="2"),
    ]

    found = find_next_class(cards, "Tue")

    assert found is not None
    assert found.card_id == "2"


def test_next_class_is_none_without_a_match() -> None:
    assert find_next_class([make_card("Thu, Aug 14")], "Tue") is None
    assert find_next_class([], "Tue") is None


@pytest.mark.parametrize(
    ("button_text", "action"),
    [
        ("Book Class", Action.CLICK_BOOK),
        ("Join Waitlist", Action.CLICK_WAITLIST),
        ("Booked", Action.ALREADY_BOOKED),
        ("Waitlisted", Action.ALREADY_WAITLISTED),
    ],
)
def test_action_follows_the_button_state(button_text: str, action: Action) -> None:
    assert decide_outcome_action(make_card(button_text=button_text)) is action


@pytest.mark.parametrize("button_text", ["Booking...", "Joining...", "Completed", "???"])
def test_action_for_busy_or_unknown_button_raises(button_text: str) -> None:
    with pytest.raises(UnknownButtonError):
        decide_outcome_action(make_card(button_text=button_text))


@pytest.mark.parametrize(
    ("outcome", "message"),
    [
        (Outcome.NEW_BOOKING, "✓ Successfully booked: Spin Class on Tomorrow (Thu, Aug 14)"),
        (Outcome.NEW_WAITLIST, "✓ Joined waitlist for: Spin Class on Tomorrow (Thu, Aug 14)"),
        (Outcome.ALREADY_BOOKED, "✓ Already booked: Spin Class on Tomorrow (Thu, Aug 14)"),
        (Outcome.ALREADY_WAITLISTED, "✓ Already on waitlist: Spin Class on Tomorrow (Thu, Aug 14)"),
    ],
)
def test_outcome_message(outcome: Outcome, message: str) -> None:
    assert format_outcome(outcome, make_card()) == message
