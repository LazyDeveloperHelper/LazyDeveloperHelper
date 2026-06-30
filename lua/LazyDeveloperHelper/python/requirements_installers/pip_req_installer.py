#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --- IMPORTS ---
import os
import sys
from subprocess import run, CalledProcessError
from logger import log_message

#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃              VARIABLES               ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
REQUIREMENTS_FILE = "requirements.txt"
ALTERNATIVE_FILE = "requirements-dev.txt"


#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃    INSTALL REQUIREMENTS FROM FILE    ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


def install_requirements(search_path="."):
    for dirpath, _, filenames in os.walk(search_path):
        if REQUIREMENTS_FILE in filenames:
            log_message(f"{REQUIREMENTS_FILE} is found!", "success")
            try:
                run(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "-r",
                        os.path.join(dirpath, REQUIREMENTS_FILE),
                    ],
                    check=True,
                )
                return True
            except CalledProcessError as e:
                log_message(f"Error installing {REQUIREMENTS_FILE}: {e}", "error")
                return False

        elif ALTERNATIVE_FILE in filenames:
            log_message(
                f"{REQUIREMENTS_FILE} not found, using {ALTERNATIVE_FILE}", "info"
            )
            try:
                run(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "-r",
                        os.path.join(dirpath, ALTERNATIVE_FILE),
                    ],
                    check=True,
                )
                return True
            except CalledProcessError as e:
                log_message(f"Error installing {ALTERNATIVE_FILE}: {e}", "error")
                return False

    log_message(
        f"{REQUIREMENTS_FILE} or {ALTERNATIVE_FILE} not found in {search_path}!",
        "error",
    )
    return False


if __name__ == "__main__":
    search_path = sys.argv[1] if len(sys.argv) > 1 else "."
    success = install_requirements(search_path)
    if not success:
        sys.exit(1)

    sys.exit(0)
