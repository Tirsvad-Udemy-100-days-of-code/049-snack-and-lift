"""@file test_credentials.py
@brief Credentials come from the environment and never show the password.
"""

import pytest

from snack_and_lift import constants
from snack_and_lift.application.credentials import (
    Credentials,
    load_admin_credentials,
    load_credentials,
)
from snack_and_lift.domain.errors import MissingCredentialsError

DUMMY_PASSWORD = "dummy-secret-value"


def test_load_credentials_reads_both_variables() -> None:
    environment = {
        constants.ACCOUNT_EMAIL_ENV: "dummy@example.invalid",
        constants.ACCOUNT_PASSWORD_ENV: DUMMY_PASSWORD,
    }

    assert load_credentials(environment) == Credentials("dummy@example.invalid", DUMMY_PASSWORD)


@pytest.mark.parametrize(
    "environment",
    [
        {},
        {constants.ACCOUNT_EMAIL_ENV: "dummy@example.invalid"},
        {constants.ACCOUNT_PASSWORD_ENV: DUMMY_PASSWORD},
        {constants.ACCOUNT_EMAIL_ENV: "", constants.ACCOUNT_PASSWORD_ENV: DUMMY_PASSWORD},
        {constants.ACCOUNT_EMAIL_ENV: "dummy@example.invalid", constants.ACCOUNT_PASSWORD_ENV: ""},
    ],
)
def test_load_credentials_rejects_missing_or_empty(environment: dict[str, str]) -> None:
    with pytest.raises(MissingCredentialsError) as caught:
        load_credentials(environment)

    message = str(caught.value)
    assert constants.ACCOUNT_EMAIL_ENV in message
    assert constants.ACCOUNT_PASSWORD_ENV in message
    assert DUMMY_PASSWORD not in message


def test_repr_hides_the_password() -> None:
    assert DUMMY_PASSWORD not in repr(Credentials("dummy@example.invalid", DUMMY_PASSWORD))


def test_load_admin_credentials_reads_both_variables() -> None:
    environment = {
        constants.ADMIN_EMAIL_ENV: " admin@example.invalid ",
        constants.ADMIN_PASSWORD_ENV: DUMMY_PASSWORD,
    }

    assert load_admin_credentials(environment) == Credentials(
        "admin@example.invalid", DUMMY_PASSWORD
    )


@pytest.mark.parametrize(
    "environment",
    [
        {},
        {constants.ADMIN_EMAIL_ENV: "", constants.ADMIN_PASSWORD_ENV: ""},
        {constants.ADMIN_EMAIL_ENV: "  "},
    ],
)
def test_load_admin_credentials_is_none_when_not_set(environment: dict[str, str]) -> None:
    assert load_admin_credentials(environment) is None


@pytest.mark.parametrize(
    ("environment", "missing"),
    [
        ({constants.ADMIN_EMAIL_ENV: "admin@example.invalid"}, constants.ADMIN_PASSWORD_ENV),
        (
            {constants.ADMIN_EMAIL_ENV: "admin@example.invalid", constants.ADMIN_PASSWORD_ENV: ""},
            constants.ADMIN_PASSWORD_ENV,
        ),
        ({constants.ADMIN_PASSWORD_ENV: DUMMY_PASSWORD}, constants.ADMIN_EMAIL_ENV),
        (
            {constants.ADMIN_EMAIL_ENV: "", constants.ADMIN_PASSWORD_ENV: DUMMY_PASSWORD},
            constants.ADMIN_EMAIL_ENV,
        ),
    ],
)
def test_load_admin_credentials_rejects_half_set(environment: dict[str, str], missing: str) -> None:
    with pytest.raises(MissingCredentialsError) as caught:
        load_admin_credentials(environment)

    message = str(caught.value)
    assert message.startswith(f"Set {missing} too")
    assert DUMMY_PASSWORD not in message
    assert "admin@example.invalid" not in message
