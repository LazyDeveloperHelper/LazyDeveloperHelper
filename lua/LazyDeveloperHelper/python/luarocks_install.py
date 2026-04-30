#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from subprocess import run, CalledProcessError
from shutil import which
from typing import Any
from logger import log_message

#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃         VARIABLES          ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

LUAROCKS_FLAG = "--local"
luarocks_path: str | None = which(cmd="luarocks")


#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃    CHECKING LIBRARY NAME    ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def validate_library_name(lib: str) -> bool:
    if not lib or any(c in lib for c in '<>|&;"'):
        log_message(f"Invalid library name: {lib}", "error")
        return False
    return True


#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃         CHECK PATH         ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


def check_path() -> str:
    if not luarocks_path:
        log_message("luarocks is not found in PATH", "error")
        raise ValueError("LuaRocks not found")
    return luarocks_path


#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃    INSTALLING BY LUAROCKS    ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def install_luarocks(libs: list[str], quiet: bool = False) -> None:
    check_path()
    for lib in libs:
        if not validate_library_name(lib):
            continue

        log_message(f"Installing LuaRocks package {lib} ...", "info")

        # Build arguments
        flags: list[str] = [LUAROCKS_FLAG]
        if quiet:
            flags.append("-q")

        luarocks_args: list[str] = [luarocks_path, "install", lib] + flags

        try:
            result: Any = run(
                args=luarocks_args,
                check=True,
                text=True,
                capture_output=True,
            )

            stdout_lower = result.stdout.lower()
            if any(msg in stdout_lower for msg in ["installed", "already installed"]):
                log_message(f"{lib} installed or already present", level="success")

            if result.stdout and not quiet:
                log_message(result.stdout, "info")
        except CalledProcessError as e:
            log_message(f"Failed to install {lib}", "error")
            log_message(f"stdout:\n{e.stdout}")

            log_message(f"stderr:\n{e.stderr}")
            log_message(f"Return code: {e.returncode}", "error")
        except FileNotFoundError as e:
            log_message(f"File error: {e}", "error")

        except PermissionError as e:
            log_message(f"Permission error: {e}", "error")


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("libs", nargs="*", help="LuaRocks packages to install")
    parser.add_argument("--quiet", action="store_true", help="Suppress output")

    args, unknown = parser.parse_known_args()

    # unknown contains anything argparse didn’t understand
    # remove any optional flags accidentally included in libs
    libs: list[Any] = [lib for lib in args.libs if not lib.startswith("--")]

    if not args.libs:
        log_message("No valid libraries provided", "error")
        sys.exit(1)
    install_luarocks(libs, quiet=args.quiet)


if __name__ == "__main__":
    main()
