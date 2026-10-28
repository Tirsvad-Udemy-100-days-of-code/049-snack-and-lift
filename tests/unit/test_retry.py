"""@file test_retry.py
@brief The retry wrapper: success, repeats, exhaustion, what it logs and what it never retries.
"""

import logging

import pytest

from snack_and_lift import constants
from snack_and_lift.application.retry import retry
from snack_and_lift.domain.errors import (
    GymError,
    LoginFailedError,
    MissingCredentialsError,
    PageFormatError,
    RetriesExhaustedError,
    UnknownButtonError,
)


class Flaky:
    """@brief A step that raises the given errors in turn and then returns a value."""

    def __init__(self, errors: list[Exception], value: str = "done") -> None:
        self._errors = list(errors)
        self._value = value
        self.calls = 0

    def __call__(self) -> str:
        self.calls += 1
        if self._errors:
            raise self._errors.pop(0)
        return self._value


def test_retry_returns_the_result_on_the_first_attempt() -> None:
    step = Flaky([])
    sleeps: list[float] = []

    assert retry(step, sleep=sleeps.append) == "done"
    assert step.calls == 1
    assert sleeps == []


def test_retry_succeeds_after_some_failures(caplog: pytest.LogCaptureFixture) -> None:
    step = Flaky([GymError("a"), GymError("b")])

    with caplog.at_level(logging.INFO):
        result = retry(step, 7, "login", sleep=lambda _: None)

    assert result == "done"
    assert step.calls == 3
    assert "✓ login succeeded after 3 attempts" in caplog.text


def test_retry_does_not_log_success_after_a_single_attempt(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.INFO):
        retry(Flaky([]), 7, "login", sleep=lambda _: None)

    assert "succeeded" not in caplog.text


def test_retry_raises_after_the_last_attempt_with_the_last_error_as_cause() -> None:
    last = GymError("third")
    step = Flaky([GymError("first"), GymError("second"), last])

    with pytest.raises(RetriesExhaustedError, match="login failed after 3 attempts") as caught:
        retry(step, 3, "login", sleep=lambda _: None)

    assert caught.value.__cause__ is last
    assert "third" in str(caught.value)
    assert step.calls == 3


def test_retries_exhausted_is_a_gym_error() -> None:
    with pytest.raises(GymError):
        retry(Flaky([GymError("x")]), 1, sleep=lambda _: None)


def test_retry_with_one_attempt_does_not_repeat_or_sleep() -> None:
    step = Flaky([GymError("x"), GymError("y")])
    sleeps: list[float] = []

    with pytest.raises(RetriesExhaustedError):
        retry(step, 1, sleep=sleeps.append)

    assert step.calls == 1
    assert sleeps == []


def test_retry_with_one_attempt_returns_on_success() -> None:
    assert retry(Flaky([]), 1, sleep=lambda _: None) == "done"


def test_retry_waits_the_delay_between_attempts_but_not_after_the_last() -> None:
    sleeps: list[float] = []

    with pytest.raises(RetriesExhaustedError):
        retry(Flaky([GymError("x")] * 4), 4, delay=1.5, sleep=sleeps.append)

    assert sleeps == [1.5, 1.5, 1.5]


def test_retry_uses_the_default_delay_and_attempts() -> None:
    sleeps: list[float] = []
    step = Flaky([GymError("x")] * constants.RETRY_COUNT)

    with pytest.raises(RetriesExhaustedError):
        retry(step, sleep=sleeps.append)

    assert step.calls == constants.RETRY_COUNT
    assert sleeps == [constants.RETRY_DELAY_SECONDS] * (constants.RETRY_COUNT - 1)


def test_retry_logs_a_warning_with_attempt_description_and_error(
    caplog: pytest.LogCaptureFixture,
) -> None:
    step = Flaky([GymError("Network request failed. Please try again.")])

    with caplog.at_level(logging.WARNING):
        retry(step, 7, "login", sleep=lambda _: None)

    assert (
        "⚠ Attempt 1/7 failed: login: Network request failed. Please try again. Retrying..."
        in caplog.text
    )


def test_retry_names_a_step_without_description(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING):
        retry(Flaky([GymError("x")]), sleep=lambda _: None)

    assert f"failed: {constants.RETRY_DEFAULT_DESCRIPTION}: x" in caplog.text


@pytest.mark.parametrize(
    "error",
    [LoginFailedError("no"), UnknownButtonError("busy"), PageFormatError("format")],
)
def test_retry_repeats_every_kind_of_gym_error(error: GymError) -> None:
    step = Flaky([error])

    assert retry(step, 2, sleep=lambda _: None) == "done"
    assert step.calls == 2


def test_retry_lets_other_errors_pass_untouched() -> None:
    error = MissingCredentialsError("missing")
    step = Flaky([error])

    with pytest.raises(MissingCredentialsError) as caught:
        retry(step, 7, sleep=lambda _: None)

    assert caught.value is error
    assert step.calls == 1


@pytest.mark.parametrize("retries", [0, -1])
def test_retry_rejects_fewer_than_one_attempt(retries: int) -> None:
    step = Flaky([])

    with pytest.raises(ValueError, match="at least 1"):
        retry(step, retries)

    assert step.calls == 0
