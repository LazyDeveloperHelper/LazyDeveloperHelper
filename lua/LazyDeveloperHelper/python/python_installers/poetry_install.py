#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import run, CalledProcessError
from shutil import which


PYPROJECT_TOML = "pyproject.toml"


# --- CHECK poetry STATUS ---
def check_poetry_installed() -> str:
    """Check if poetry is installed and available in PATH."""
    poetry_path: str | None = which("poetry")
    if poetry_path is None:
        log_message("Poetry is not installed or not found in PATH.", "error")
        return str(poetry_path)
    return poetry_path


# --- LOGGING MESSAGE ---
def log_message(message: str, level: str = "info"):
    prefixes = {
        "info": chr(0x1F4CD),  # 📍
        "success": chr(0x1F4E6),  # 📦
        "error": chr(0x274C),  # ❌
    }

    print(f"{prefixes.get(level, '\u0001f4cd')} {message}")


# --- FIND pyproject.toml ---
def find_pyproject(start_dir: str = ".") -> str | None:
    """
    Find pyproject.toml in current or parent directories.
    Returns abs path or None.
    """
    pyproject_path = os.path.join(start_dir, PYPROJECT_TOML)
    if os.path.exists(path=pyproject_path):
        abs_path = os.path.abspath(pyproject_path)
        log_message(f"Found pyproject.toml at: {abs_path}", "info")
        return abs_path

    current_dir = os.path.abspath(start_dir)

    while True:
        pyproject_path = os.path.join(current_dir, PYPROJECT_TOML)
        if os.path.exists(pyproject_path):
            log_message(f"Found pyproject.toml at: {pyproject_path}", "info")
            return pyproject_path

        parent = os.path.dirname(current_dir)
        if parent == current_dir:  # Root-directory
            break
        current_dir = parent

    # not found anywhere - create in original directory
    log_message("pyproject.toml not found, creating...", "error")
    target_dir: str = os.path.abspath(
        start_dir
    )  # ← using start_dir, but not current_dir
    if os.path.exists(target_dir):
        # If directory exists → poetry init (creates pyproject.toml inside)
        _ = run(
            args=["poetry", "init", "--no-interaction"],
            check=True,
            text=True,
            cwd=target_dir,
        )
    else:
        # Other cases → poetry new (creates everything)
        _ = run(
            args=["poetry", "new", "--src", target_dir],
            check=True,
            text=True,
        )

    return os.path.join(target_dir, PYPROJECT_TOML)


# --- INSTALL DEPENDENCIES ---
def install_package(package: str):
    if not check_poetry_installed():
        return
    if not find_pyproject():
        return

    poetry_path: str = check_poetry_installed()
    cmd: list[str] = [poetry_path, "add", package]
    try:
        _ = run(args=cmd, check=True, capture_output=True, text=True)
        log_message(f"{package} installed/added.", "success")
    except CalledProcessError as e:
        log_message(f"Failed: {e.stderr}", "error")


if __name__ == "__main__":
    packages = sys.argv[1]
    if not packages:
        log_message("Please provide any package!", "error")
    install_package(packages)
