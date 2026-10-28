"""@file test_resilience.py
@brief Lecture step 9: login, booking and bookings read survive a site that drops requests.
"""

import logging
import random
from pathlib import Path

import pytest
from tests.unit.fakes import ChaosGym, FakeGym, no_sleep
from tests.unit.test_booking_entry import make_entry
from tests.unit.test_models import make_card

from snack_and_lift import constants
from snack_and_lift.application.booking import (
    book_class_with_retry,
    book_next_tuesday,
    book_target_classes,
)
from snack_and_lift.application.credentials import Credentials
from snack_and_lift.application.session import login_with_retry
from snack_and_lift.application.verification import get_my_bookings_with_retry, verify_bookings
from snack_and_lift.cli import main, parse_args
from snack_and_lift.domain.errors import GymError, LoginFailedError, RetriesExhaustedError
from snack_and_lift.domain.models import ButtonState, ClassResult, Outcome

DUMMY_EMAIL = "dummy@example.invalid"
DUMMY_PASSWORD = "dummy-password"
CREDENTIALS = Credentials(DUMMY_EMAIL, DUMMY_PASSWORD)


@pytest.fixture
def credentials_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(constants.ACCOUNT_EMAIL_ENV, DUMMY_EMAIL)
    monkeypatch.setenv(constants.ACCOUNT_PASSWORD_ENV, DUMMY_PASSWORD)


def test_login_with_retry_logs_in_after_two_dropped_requests(
    caplog: pytest.LogCaptureFixture,
) -> None:
    gym = FakeGym(fail_first={"log_in": 2})
    sleeps: list[float] = []

    with caplog.at_level(logging.INFO):
        login_with_retry(gym, CREDENTIALS, sleep=sleeps.append)

    assert gym.calls == ["log_in"] * 3
    assert sleeps == [constants.RETRY_DELAY_SECONDS] * 2
    assert "⚠ Attempt 2/7 failed: login: Network request failed. Please try again." in caplog.text
    assert "✓ login succeeded after 3 attempts" in caplog.text


def test_login_with_retry_never_logs_the_password(caplog: pytest.LogCaptureFixture) -> None:
    gym = FakeGym(fail_first={"log_in": 2})

    with caplog.at_level(logging.DEBUG):
        login_with_retry(gym, CREDENTIALS, sleep=no_sleep)

    assert DUMMY_PASSWORD not in caplog.text
    assert DUMMY_EMAIL not in caplog.text


def test_login_with_retry_gives_up_after_the_set_attempts() -> None:
    gym = FakeGym(fail_first={"log_in": 10})

    with pytest.raises(RetriesExhaustedError, match="login failed after 3 attempts") as caught:
        login_with_retry(gym, CREDENTIALS, retries=3, sleep=no_sleep)

    assert isinstance(caught.value.__cause__, LoginFailedError)
    assert len(gym.logins) == 3


def test_book_class_with_retry_repeats_a_dropped_click() -> None:
    card = make_card()
    gym = FakeGym(cards=[card], fail_first={"press_class_button": 2})

    result = book_class_with_retry(gym, card, sleep=no_sleep)

    assert result.outcome is Outcome.NEW_BOOKING
    assert gym.pressed == ["123", "123", "123"]
    assert gym.calls.count("list_class_cards") == 2


def test_book_class_with_retry_reads_nothing_again_when_the_first_attempt_works() -> None:
    card = make_card()
    gym = FakeGym(cards=[card])

    book_class_with_retry(gym, card, sleep=no_sleep)

    assert gym.calls == ["press_class_button"]


@pytest.mark.parametrize(
    ("button_text", "outcome", "final_state"),
    [
        ("Book Class", Outcome.NEW_BOOKING, ButtonState.BOOKED),
        ("Join Waitlist", Outcome.NEW_WAITLIST, ButtonState.WAITLISTED),
    ],
)
def test_book_class_with_retry_counts_a_click_that_went_through_as_new(
    button_text: str,
    outcome: Outcome,
    final_state: ButtonState,
    caplog: pytest.LogCaptureFixture,
) -> None:
    card = make_card(button_text=button_text)
    gym = FakeGym(cards=[card], fail_first={"press_class_button": 1}, click_goes_through=True)

    with caplog.at_level(logging.INFO):
        result = book_class_with_retry(gym, card, sleep=no_sleep)

    assert result.outcome is outcome
    assert gym.pressed == ["123"]
    assert gym.cards[0].state is final_state
    assert "Already" not in caplog.text


def test_book_class_with_retry_keeps_already_booked_as_it_is() -> None:
    card = make_card(button_text="Booked")
    gym = FakeGym(cards=[card])

    result = book_class_with_retry(gym, card, sleep=no_sleep)

    assert result.outcome is Outcome.ALREADY_BOOKED
    assert gym.pressed == []


def test_book_class_with_retry_does_not_count_a_click_without_confirmation() -> None:
    card = make_card()
    gym = FakeGym(cards=[card], press_result="Book Class")

    with pytest.raises(RetriesExhaustedError, match="click not confirmed"):
        book_class_with_retry(gym, card, retries=2, sleep=no_sleep)

    assert gym.pressed == ["123", "123"]


def test_book_class_with_retry_fails_when_the_class_left_the_schedule() -> None:
    card = make_card()
    gym = FakeGym(cards=[card], fail_first={"press_class_button": 1})
    gym.cards.clear()

    with pytest.raises(RetriesExhaustedError, match="not found on the schedule"):
        book_class_with_retry(gym, card, retries=2, sleep=no_sleep)


def test_book_class_with_retry_gives_up_after_the_set_attempts() -> None:
    card = make_card()
    gym = FakeGym(cards=[card], fail_first={"press_class_button": 9})

    with pytest.raises(RetriesExhaustedError, match="book Spin Class on Tomorrow"):
        book_class_with_retry(gym, card, retries=3, sleep=no_sleep)

    assert len(gym.pressed) == 3


def test_book_next_tuesday_repeats_a_dropped_click() -> None:
    gym = FakeGym(cards=[make_card("Tue, Aug 19")], fail_first={"press_class_button": 1})

    result = book_next_tuesday(gym, sleep=no_sleep)

    assert result is not None
    assert result.outcome is Outcome.NEW_BOOKING


def test_book_target_classes_repeats_each_class_on_its_own() -> None:
    gym = FakeGym(
        cards=[make_card("Thu, Aug 14", card_id="1"), make_card("Tue, Aug 19", card_id="2")],
        fail_first={"press_class_button": 3},
    )

    results = book_target_classes(gym, sleep=no_sleep)

    assert [result.outcome for result in results] == [Outcome.NEW_BOOKING] * 2
    assert gym.pressed == ["1", "1", "1", "1", "2"]


def test_get_my_bookings_with_retry_opens_the_page_again_after_a_failure() -> None:
    entries = [make_entry("Wed, Aug 13, 7:00 AM")]
    gym = FakeGym(bookings=entries, fail_first={"open_my_bookings": 1, "list_my_bookings": 1})

    assert get_my_bookings_with_retry(gym, sleep=no_sleep) == entries
    assert gym.calls == [
        "open_my_bookings",
        "open_my_bookings",
        "list_my_bookings",
        "open_my_bookings",
        "list_my_bookings",
    ]


def test_get_my_bookings_with_retry_gives_up_after_the_set_attempts() -> None:
    gym = FakeGym(bookings_error="Failed to load bookings")

    with pytest.raises(RetriesExhaustedError, match="Failed to load bookings"):
        get_my_bookings_with_retry(gym, retries=2, sleep=no_sleep)


def test_verify_bookings_reads_the_page_through_retry() -> None:
    card = make_card("Tue, Aug 12")
    gym = FakeGym(cards=[card], fail_first={"list_my_bookings": 2})
    results = [ClassResult(card, Outcome.NEW_BOOKING)]

    verification = verify_bookings(gym, results, sleep=no_sleep)

    assert verification.is_success


def test_main_completes_a_run_with_dropped_requests_and_draws_them_in_step_9(
    credentials_env: None, tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    gym = FakeGym(
        cards=[make_card("Thu, Aug 14", card_id="1"), make_card("Tue, Aug 19", card_id="2")],
        fail_first={"log_in": 1, "press_class_button": 2, "list_my_bookings": 1},
    )

    with caplog.at_level(logging.INFO):
        code = main(["--screenshot-dir", str(tmp_path)], lambda *_: gym, no_sleep)

    assert code == 0
    step_9, step_9_path = gym.text_screenshots[-1]
    assert step_9_path == tmp_path / "step-9.png"
    assert "⚠ Attempt 1/7 failed: login" in step_9
    assert "succeeded after 2 attempts" in step_9
    assert step_9.endswith("✅ SUCCESS: All bookings verified!")


def test_main_returns_1_when_every_retry_failed(
    credentials_env: None, caplog: pytest.LogCaptureFixture
) -> None:
    gym = FakeGym(fail_first={"log_in": 5})

    with caplog.at_level(logging.INFO):
        code = main(["--retries", "2"], lambda *_: gym, no_sleep)

    assert code == 1
    assert len(gym.logins) == 2
    assert "Failed: login failed after 2 attempts" in caplog.text


def test_main_uses_one_attempt_when_asked() -> None:
    assert parse_args(["--retries", "1"]).retries == 1


def test_retries_option_defaults_to_the_constant() -> None:
    assert parse_args([]).retries == constants.RETRY_COUNT


@pytest.mark.parametrize("value", ["0", "-3", "many", "1.5"])
def test_retries_option_rejects_less_than_one(value: str) -> None:
    with pytest.raises(SystemExit):
        parse_args(["--retries", value])


def test_help_epilog_mentions_retries(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        parse_args(["--help"])

    out = capsys.readouterr().out
    assert "--retries N" in out
    assert "every retry failed" in out


## Chance that a request fails in the chaos test: the site's maximum (50%).
CHAOS_FAILURE_PROBABILITY = 0.5

## Chaos runs, and how many must complete. With 7 attempts an operation fails for good with
## probability 0.5**7 (about 0.8%). A run has four such operations (login, two clicks, the
## bookings read), so about 3% of runs fail and about 97 of 100 complete; 90 leaves room for
## the spread of the seeds without hiding a real defect. The seeds are fixed, so it is stable.
CHAOS_RUNS = 100
CHAOS_MIN_COMPLETED = 90

## Seeds that were checked to complete fully (seed 18 is the first that runs out of attempts);
## a change that breaks one of them is a defect.
CHAOS_SEEDS_THAT_MUST_PASS = tuple(range(18))


def _run_chaos(seed: int) -> tuple[int, ChaosGym]:
    gym = ChaosGym(
        random.Random(seed),
        CHAOS_FAILURE_PROBABILITY,
        cards=[make_card("Thu, Aug 14", card_id="1"), make_card("Tue, Aug 19", card_id="2")],
    )
    return main(["--retries", "7"], lambda *_: gym, no_sleep), gym


def _is_consistent(gym: ChaosGym) -> bool:
    """@brief True when every target class is booked on the page after the run."""
    return all(card.state is ButtonState.BOOKED for card in gym.cards)


@pytest.mark.usefixtures("credentials_env")
def test_chaos_runs_with_half_of_the_requests_failing_mostly_complete() -> None:
    completed = 0
    for seed in range(CHAOS_RUNS):
        code, gym = _run_chaos(seed)
        assert code in (0, 1), f"seed {seed}: a verified run never ends in a mismatch"
        if code == 0:
            assert _is_consistent(gym), f"seed {seed}: verified but not booked"
            completed += 1

    assert completed >= CHAOS_MIN_COMPLETED


@pytest.mark.usefixtures("credentials_env")
@pytest.mark.parametrize("seed", CHAOS_SEEDS_THAT_MUST_PASS)
def test_chaos_seed_completes_with_a_consistent_verified_result(seed: int) -> None:
    code, gym = _run_chaos(seed)

    assert code == 0
    assert _is_consistent(gym)


def test_retry_error_is_a_gym_error_for_the_exit_code() -> None:
    assert issubclass(RetriesExhaustedError, GymError)
