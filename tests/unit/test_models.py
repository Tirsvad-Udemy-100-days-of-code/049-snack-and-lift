"""@file test_models.py
@brief Button states and the values derived from a class card.
"""

import dataclasses

import pytest

from snack_and_lift.domain.errors import PageFormatError
from snack_and_lift.domain.models import ButtonState, ClassCard


def make_card(
    day_label: str = "Tomorrow (Thu, Aug 14)",
    time_text: str = "Time: 6:00 PM",
    button_text: str = "Book Class",
    card_id: str = "123",
    name: str = "Spin Class",
) -> ClassCard:
    return ClassCard(card_id, name, day_label, time_text, button_text)


@pytest.mark.parametrize(
    ("text", "state"),
    [
        ("Book Class", ButtonState.BOOK),
        ("Join Waitlist", ButtonState.JOIN_WAITLIST),
        ("Booked", ButtonState.BOOKED),
        ("Waitlisted", ButtonState.WAITLISTED),
        ("Booking...", ButtonState.BUSY),
        ("Joining...", ButtonState.BUSY),
        ("Completed", ButtonState.COMPLETED),
        (" Booked ", ButtonState.BOOKED),
        ("", ButtonState.UNKNOWN),
        ("Cancel", ButtonState.UNKNOWN),
    ],
)
def test_button_state_is_read_from_text(text: str, state: ButtonState) -> None:
    assert ButtonState.from_text(text) is state


def test_card_derives_state_weekday_and_date() -> None:
    card = make_card()

    assert card.state is ButtonState.BOOK
    assert card.weekday == "Thu"
    assert card.date_text == "Thu, Aug 14"


def test_card_with_bad_day_label_raises() -> None:
    with pytest.raises(PageFormatError):
        _ = make_card(day_label="Someday").weekday


def test_card_is_immutable() -> None:
    with pytest.raises(dataclasses.FrozenInstanceError):
        make_card().name = "Other"  # type: ignore[misc]
