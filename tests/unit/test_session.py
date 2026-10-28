"""@file test_session.py
@brief The login use case hands the credentials to the gym site.
"""

import pytest
from tests.unit.fakes import FakeGym

from snack_and_lift.application.credentials import Credentials
from snack_and_lift.application.session import login
from snack_and_lift.domain.errors import LoginFailedError

CREDENTIALS = Credentials("dummy@example.invalid", "dummy-password")


def test_login_passes_the_credentials_to_the_gym() -> None:
    gym = FakeGym()

    login(gym, CREDENTIALS)

    assert gym.logins == [("dummy@example.invalid", "dummy-password")]


def test_login_propagates_a_refused_login() -> None:
    gym = FakeGym(login_error="Invalid credentials")

    with pytest.raises(LoginFailedError, match="Invalid credentials"):
        login(gym, CREDENTIALS)
