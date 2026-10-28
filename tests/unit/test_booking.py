"""@file test_booking.py
@brief Booking a class and booking the next Tuesday class, against a fake gym.
"""

import logging

import pytest
from tests.unit.fakes import FakeGym, no_sleep
from tests.unit.test_models import make_card

from snack_and_lift.application.booking import (
    book_class,
    book_next_tuesday,
    book_target_classes,
)
from snack_and_lift.domain.errors import GymError, UnknownButtonError
from snack_and_lift.domain.models import Outcome


@pytest.mark.parametrize(
    ("button_text", "outcome", "message"),
    [
        ("Book Class", Outcome.NEW_BOOKING, "✓ Successfully booked: Spin Class on"),
        ("Join Waitlist", Outcome.NEW_WAITLIST, "✓ Joined waitlist for: Spin Class on"),
    ],
)
def test_book_class_clicks_and_confirms(
    button_text: str, outcome: Outcome, message: str, caplog: pytest.LogCaptureFixture
) -> None:
    card = make_card(button_text=button_text)
    gym = FakeGym(cards=[card])

    with caplog.at_level(logging.INFO):
        result = book_class(gym, card)

    assert result.outcome is outcome
    assert gym.pressed == ["123"]
    assert message in caplog.text


@pytest.mark.parametrize(
    ("button_text", "outcome"),
    [("Booked", Outcome.ALREADY_BOOKED), ("Waitlisted", Outcome.ALREADY_WAITLISTED)],
)
def test_book_class_does_not_click_when_already_done(button_text: str, outcome: Outcome) -> None:
    gym = FakeGym()

    result = book_class(gym, make_card(button_text=button_text))

    assert result.outcome is outcome
    assert gym.pressed == []


def test_book_class_raises_when_click_is_not_confirmed() -> None:
    card = make_card()
    gym = FakeGym(cards=[card], press_result="Book Class")

    with pytest.raises(GymError, match="click not confirmed"):
        book_class(gym, card)


def test_book_class_raises_when_waitlist_click_gives_booked() -> None:
    card = make_card(button_text="Join Waitlist")

    with pytest.raises(GymError, match="click not confirmed"):
        book_class(FakeGym(cards=[card], press_result="Booked"), card)


def test_book_class_propagates_a_site_error() -> None:
    with pytest.raises(GymError, match="Network down"):
        book_class(FakeGym(cards=[make_card()], press_error="Network down"), make_card())


def test_book_class_raises_for_a_busy_button() -> None:
    with pytest.raises(UnknownButtonError):
        book_class(FakeGym(), make_card(button_text="Booking..."))


def test_book_next_tuesday_books_the_first_tuesday_class() -> None:
    cards = [
        make_card("Today (Wed, Aug 13)", card_id="1"),
        make_card("Tue, Aug 19", card_id="2"),
        make_card("Tue, Aug 26", card_id="3"),
    ]
    gym = FakeGym(cards=cards)

    result = book_next_tuesday(gym)

    assert result is not None
    assert result.card.card_id == "2"
    assert gym.pressed == ["2"]


def test_book_next_tuesday_logs_when_there_is_no_class(caplog: pytest.LogCaptureFixture) -> None:
    gym = FakeGym(cards=[make_card("Wed, Aug 13")])

    with caplog.at_level(logging.INFO):
        assert book_next_tuesday(gym) is None

    assert "No Tue class at 18:00 found" in caplog.text
    assert gym.pressed == []


def test_book_target_classes_handles_every_target_class_in_order() -> None:
    cards = [
        make_card("Today (Wed, Aug 13)", card_id="1"),
        make_card("Tomorrow (Thu, Aug 14)", card_id="2"),
        make_card("Tue, Aug 19", card_id="3", button_text="Join Waitlist"),
        make_card("Thu, Aug 21", card_id="4", button_text="Booked"),
        make_card("Tue, Aug 26", card_id="5", button_text="Waitlisted"),
    ]
    gym = FakeGym(cards=cards)

    results = book_target_classes(gym)

    assert [result.outcome for result in results] == [
        Outcome.NEW_BOOKING,
        Outcome.NEW_WAITLIST,
        Outcome.ALREADY_BOOKED,
        Outcome.ALREADY_WAITLISTED,
    ]
    assert gym.pressed == ["2", "3"]
    assert gym.calls.count("list_class_cards") == 1


def test_book_target_classes_calls_back_after_each_class() -> None:
    gym = FakeGym(
        cards=[make_card("Thu, Aug 14", card_id="1"), make_card("Tue, Aug 19", card_id="2")]
    )
    seen: list[str] = []

    book_target_classes(gym, lambda result: seen.append(result.card.card_id))

    assert seen == ["1", "2"]


def test_book_target_classes_logs_when_there_is_none(caplog: pytest.LogCaptureFixture) -> None:
    gym = FakeGym(cards=[make_card("Wed, Aug 13")])

    with caplog.at_level(logging.INFO):
        assert book_target_classes(gym) == []

    assert "No Tuesday or Thursday class at 18:00 found" in caplog.text


def test_book_target_classes_propagates_a_failing_class() -> None:
    gym = FakeGym(cards=[make_card("Thu, Aug 14")], press_error="Network down")

    with pytest.raises(GymError, match="Network down"):
        book_target_classes(gym, sleep=no_sleep)
