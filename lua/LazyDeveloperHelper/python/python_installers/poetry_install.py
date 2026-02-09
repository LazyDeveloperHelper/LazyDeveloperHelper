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
    poetry_path = str(which("poetry"))
    if poetry_path is None:
        log_message("Poetry is not installed or not found in PATH.", "error")
        return poetry_path
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
def find_pyproject(start_dir="."):
    """Find pyproject.toml in current or parent directories. Returns abs path or None."""
    cargo_path = os.path.join(start_dir, PYPROJECT_TOML)  # Typo fix: pyproject
    if os.path.exists(cargo_path):
        abs_path = os.path.abspath(cargo_path)
        log_message(f"Found pyproject.toml at: {abs_path}", "info")
        return abs_path

    current_dir = os.path.abspath(start_dir)
    while current_dir != os.path.dirname(current_dir):  # Stop at root "/"
        parent_dir = os.path.dirname(current_dir)
        pyproject_path = os.path.join(parent_dir, PYPROJECT_TOML)
        if os.path.exists(pyproject_path):
            abs_path = os.path.abspath(pyproject_path)
            log_message(f"Found pyproject.toml at: {abs_path}", "info")
            return abs_path
        current_dir = parent_dir

    log_message("pyproject.toml not found in current or parent directories.", "error")
    return None


# --- INSTALL DEPENDENCIES ---
def install_package(package: str):
    if not check_poetry_installed():
        return
    poetry_path = check_poetry_installed()
    cmd = [poetry_path, "add", package]
    try:
        run(cmd, check=True, capture_output=True, text=True)
        log_message(f"{package} installed/added.", "success")
    except CalledProcessError as e:
        log_message(f"Failed: {e.stderr}", "error")


if __name__ == "__main__":
    packages = sys.argv[1]
    if not packages:
        log_message("Please provide any package!", "error")
    install_package(packages)
