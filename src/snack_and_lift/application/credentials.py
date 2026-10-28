"""@file credentials.py
@brief The account the bot logs in with, read from the environment (never from the code).
"""

from collections.abc import Mapping
from dataclasses import dataclass, field

from snack_and_lift import constants
from snack_and_lift.domain.errors import MissingCredentialsError


@dataclass(frozen=True, slots=True)
class Credentials:
    """@brief E-mail and password of the gym account; the password is never printed."""

    email: str
    password: str = field(repr=False)


def load_credentials(environment: Mapping[str, str]) -> Credentials:
    """@brief Read the account from the environment.

    @param environment The environment variables, for example `os.environ`.
    @return The credentials.
    @exception MissingCredentialsError A variable is missing or empty; the message names
        the variables and never a value.
    """
    email = environment.get(constants.ACCOUNT_EMAIL_ENV, "").strip()
    password = environment.get(constants.ACCOUNT_PASSWORD_ENV, "")
    if not email or not password:
        raise MissingCredentialsError(
            f"Set {constants.ACCOUNT_EMAIL_ENV} and {constants.ACCOUNT_PASSWORD_ENV} "
            "in the environment (they must not be empty)"
        )
    return Credentials(email=email, password=password)
