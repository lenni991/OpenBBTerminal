import json
from enum import Enum
from typing import Any, Optional

import matplotlib.pyplot as plt

import openbb_terminal.core.session.hub_model as Hub
import openbb_terminal.core.session.local_model as Local
from openbb_terminal.base_helpers import (
    remove_log_handlers,
)
from openbb_terminal.core.models.user_model import (
    CredentialsModel,
    PreferencesModel,
    ProfileModel,
    UserModel,
)
from openbb_terminal.core.session.current_user import (
    set_current_user,
)
from openbb_terminal.core.session.preferences_handler import set_preference
from openbb_terminal.helper_funcs import system_clear
from openbb_terminal.rich_config import console

# pylint: disable=consider-using-f-string


class LoginStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    NO_RESPONSE = "no_response"
    UNAUTHORIZED = "unauthorized"


def create_session(email: str, password: str, save: bool) -> dict[Any, Any]:
    """Create a session.

    Parameters
    ----------
    email : str
        The email.
    password : str
        The password.
    save : bool
        Save the session.
    """

    session = Hub.get_session(email, password)
    if session and save:
        Local.save_session(session)
    return session


def create_session_from_token(token: str, save: bool) -> dict[Any, Any]:
    """Create a session from token.

    Parameters
    ----------
    token : str
        The token.
    save : bool
        Save the session.
    """

    session = Hub.get_session_from_token(token)
    if session and save:
        Local.save_session(session)
    return session


def login(session: dict) -> LoginStatus:
    """Login and load user info.

    Parameters
    ----------
    session : dict
        The session info.
    """

    # create a new user
    hub_user = UserModel(  # type: ignore
        credentials=CredentialsModel(),
        profile=ProfileModel(),
        preferences=PreferencesModel(),
    )
    response = Hub.fetch_user_configs(session)
    if response is not None:
        if response.status_code == 200:
            configs = json.loads(response.content)
            email = configs.get("email", "")
            feature_settings = configs.get("features_settings", {})
            hub_user.profile.load_user_info(session, email)
            set_current_user(hub_user)
            Local.apply_configs(configs=configs)
            if feature_settings.get("FLAIR", None) is None:
                MAX_FLAIR_LEN = 20
                flair = "[" + hub_user.profile.username[:MAX_FLAIR_LEN] + "]" + " 🦋"
                set_preference("FLAIR", flair, login=True)
            return LoginStatus.SUCCESS
        if response.status_code == 401:
            return LoginStatus.UNAUTHORIZED
        return LoginStatus.FAILED
    return LoginStatus.NO_RESPONSE


def logout(
    auth_header: Optional[str] = None,
    token: Optional[str] = None,
    guest: bool = True,
    cls: bool = False,
):
    """Logout and clear session.

    Parameters
    ----------
    auth_header : str, optional
        The authorization header, e.g. "Bearer <token>".
    token : str, optional
        The token to delete.
        In the terminal we want to delete the current session, so we use the user own token.
    guest : bool
        True if the user is guest, False otherwise.
    cls : bool
        Clear the screen.
    """
    if cls:
        system_clear()

    success = True
    if not guest:
        if not auth_header or not token:
            return

        r = Hub.delete_session(auth_header, token)
        if not r or r.status_code != 200:
            success = False

        if not Local.remove_session_file():
            success = False

    if not Local.remove_cli_history_file():
        success = False

    remove_log_handlers()

    plt.close("all")

    if success:
        console.print("[green]\nLogout successful.[/green]")
