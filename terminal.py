import sys
from multiprocessing import freeze_support

import openbb_terminal.core.session.current_user as _  # noqa: F401
from openbb_terminal.base_helpers import load_env_files
from openbb_terminal.core.config.paths_helper import init_userdata
from openbb_terminal.terminal_helper import is_auth_enabled

# pylint: disable=import-outside-toplevel


def main():
    sent_args = sys.argv[1:]

    load_env_files()
    init_userdata()

    if "-t" in sent_args or "--test" in sent_args:
        from openbb_terminal.core.integration_tests import integration_controller

        integration_controller.main()
    else:
        from openbb_terminal.core.session import session_controller

        if is_auth_enabled():
            session_controller.main()
        else:
            session_controller.launch_terminal()


if __name__ == "__main__":
    freeze_support()
    main()
