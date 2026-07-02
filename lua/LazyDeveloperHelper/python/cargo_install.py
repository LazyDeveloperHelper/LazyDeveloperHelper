#!/bin/env python3
# --- IMPORTS ---
import os
import sys
from subprocess import run, CalledProcessError
from shutil import which
from functools import lru_cache
from logger import logger


# --- VARIABLES ---
CARGO_TOML = "Cargo.toml"
cargo_path = which("cargo")


# --- CACHE Cargo.toml LOCATION ---
@lru_cache(maxsize=1)
def find_cargo_toml(start_dir: str = ".") -> str | None:
    """Search for Cargo.toml starting from the specified directory.

    Args:
        start_dir (str): Directory to start the search from. Defaults to current directory.

    Returns:
        str | None: Absolute path to Cargo.toml if found, None otherwise.
    """
    cargo_path = os.path.join(start_dir, CARGO_TOML)
    if os.path.exists(cargo_path):
        abs_path = os.path.abspath(cargo_path)
        logger(f"Found Cargo.toml at: {abs_path}", "info")
        return abs_path
    # --- IF Cargo.toml IS FOUND
    current_dir = os.path.abspath(start_dir)
    while current_dir != os.path.dirname(current_dir):
        parent_dir = os.path.dirname(current_dir)
        cargo_path = os.path.join(parent_dir, CARGO_TOML)
        if os.path.exists(cargo_path):
            abs_path = os.path.abspath(cargo_path)
            logger(f"Found Cargo.toml at: {abs_path}", "info")
            return abs_path
        current_dir = parent_dir
    logger("Cargo.toml not found in current or parent directories.", "error")
    return None


# --- CHEKING CARGO INSTALLED ---
def check_cargo_installed() -> bool:
    """Check if cargo is installed and available in PATH."""
    if not cargo_path:
        logger("cargo is not installed or not found in PATH.", "error")
        return False
    logger(f"Cargo found at: {cargo_path}", "info")
    return True


# --- VALIDATE LIB NAME ---
def validate_library_name(lib: str) -> bool:
    """Check if the library name is valid."""
    if not lib or any(c in lib for c in '<>|&;"'):
        logger(f"Invalid library name: {lib}", "error")
        return False
    return True


# --- INSTALLING LIBS ---
def cargo_install(libs: list[str], quiet: bool = False) -> None:
    cargo_toml_path = find_cargo_toml()
    if not cargo_toml_path:
        return

    abs_cargo_dir = os.path.dirname(cargo_toml_path)
    original_dir = os.getcwd()
    try:
        os.chdir(abs_cargo_dir)
        logger(f"Running cargo add {' '.join(libs)} from {os.getcwd()} ...")
        cargo_args = [cargo_path, "add"] + libs
        if quiet:
            cargo_args.append("--quiet")

        result = run(
            cargo_args,
            check=True,
            capture_output=True,
            text=True,
        )
        logger("Cargo output:\n" + result.stdout, "success")
    except CalledProcessError as e:
        logger(f"Failed to install {', '.join(libs)}", "error")
        logger("stdout:\n" + e.stdout)
        logger("stderr:\n" + e.stderr)
    finally:
        os.chdir(original_dir)


def main() -> None:
    """Install Rust libraries using cargo add.
    Args: libs (list[str]): List of library names to install."""

    if len(sys.argv) < 2:
        logger("Provide at least one library name", "error")
        sys.exit(1)

    quiet = False
    libs_to_install = []

    for arg in sys.argv[1:]:
        if arg == "-quiet":
            quiet = True
        else:
            libs_to_install.append(arg)

    for _ in libs_to_install:
        cargo_install(libs_to_install, quiet=quiet)


if __name__ == "__main__":
    main()
