# IMPORTATION STANDARD


# IMPORTATION THIRDPARTY
import pytest

# IMPORTATION INTERNAL
from openbb_terminal.core.session.current_user import (
    PreferencesModel,
    copy_user,
)
from openbb_terminal.settings_controller import SettingsController

# pylint: disable=W0621


@pytest.fixture()
def controller(mocker):
    preferences = PreferencesModel(USE_PROMPT_TOOLKIT=True)
    mock_current_user = copy_user(preferences=preferences)
    mocker.patch(
        target="openbb_terminal.core.session.current_user.__current_user",
        new=mock_current_user,
    )

    mocker.patch(
        target="openbb_terminal.settings_controller.set_preference",
    )

    mocker.patch("openbb_terminal.settings_controller.session", True)
    return SettingsController()


@pytest.mark.parametrize(
    "other", [["sources.json.default"], ["-v", "sources.json.default"]]
)
def test_source(controller, other):
    controller.call_source(other)


def test_print_help(controller):
    controller.print_help()


def test_call_dt(controller):
    controller.call_dt(None)


def test_call_autoscaling(controller):
    controller.call_autoscaling(None)


@pytest.mark.parametrize("other", [["45"], ["-v", "45"]])
def test_call_dpi(controller, other):
    controller.call_dpi(other)


@pytest.mark.parametrize("other", [["45"], ["-v", "45"]])
def test_call_height(controller, other):
    controller.call_height(other)


@pytest.mark.parametrize("other", [["45"], ["-v", "45"]])
def test_call_width(controller, other):
    controller.call_width(other)


@pytest.mark.parametrize("other", [["45"], ["-v", "45"]])
def test_call_pheight(controller, other):
    controller.call_pheight(other)


@pytest.mark.parametrize("other", [["45"], ["-v", "45"]])
def test_call_pwidth(controller, other):
    controller.call_pwidth(other)


@pytest.mark.parametrize("other", [["45"], ["-v", "45"]])
def test_call_monitor(controller, other):
    controller.call_monitor(other)


@pytest.mark.parametrize("other", [["GTK3Agg"], ["-v", "GTK3Agg"], ["None"]])
def test_call_backend(controller, other):
    controller.call_backend(other)


def test_call_flair(controller):
    controller.call_flair(["😀"])
