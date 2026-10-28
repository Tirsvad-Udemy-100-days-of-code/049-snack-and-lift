"""@file retry.py
@brief Lecture step 9: repeat a step that failed because the site dropped a request.
"""

import logging
import time
from collections.abc import Callable

from snack_and_lift import constants
from snack_and_lift.domain.errors import GymError, RetriesExhaustedError

logger = logging.getLogger(__name__)

## Waits for a number of seconds; tests pass a recorder so that they never really sleep.
Sleep = Callable[[float], None]


def retry[T](
    func: Callable[[], T],
    retries: int = constants.RETRY_COUNT,
    description: str | None = None,
    *,
    delay: float = constants.RETRY_DELAY_SECONDS,
    sleep: Sleep = time.sleep,
) -> T:
    """@brief Call a function until it succeeds, at most `retries` times.

    Only a `GymError` is repeated: it is what a dropped request looks like. Any other error,
    such as missing credentials, is a defect and passes through at once.

    @param func The step, called without arguments.
    @param retries The most attempts to make, at least 1.
    @param description What the step does, for the log (never put a secret in it).
    @param delay Seconds to wait between two attempts.
    @param sleep Waits for a number of seconds.
    @return What the function returned on its first successful attempt.
    @exception ValueError `retries` is below 1.
    @exception RetriesExhaustedError Every attempt raised a `GymError`; the last one is the cause.
    """
    if retries < 1:
        raise ValueError(constants.MESSAGE_RETRIES_INVALID.format(retries=retries))
    name = description or constants.RETRY_DEFAULT_DESCRIPTION
    for attempt in range(1, retries + 1):
        try:
            result = func()
        except GymError as error:
            if attempt == retries:
                message = constants.MESSAGE_RETRIES_EXHAUSTED.format(
                    description=name, retries=retries, error=error
                )
                raise RetriesExhaustedError(message) from error
            logger.warning(
                constants.MESSAGE_RETRY_FAILED.format(
                    attempt=attempt,
                    retries=retries,
                    description=name,
                    error=str(error).rstrip("."),
                )
            )
            sleep(delay)
        else:
            if attempt > 1:
                logger.info(
                    constants.MESSAGE_RETRY_SUCCEEDED.format(description=name, attempts=attempt)
                )
            return result
    raise AssertionError("unreachable: the last attempt returns or raises")  # pragma: no cover
