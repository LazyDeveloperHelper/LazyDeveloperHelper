#!/bin/env python3

#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from shutil import which
import os
from functools import lru_cache
import subprocess

#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃                      VARIABLES                       ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
CARGO_TOML = "Cargo.toml"
CARGO_PATH = which("cargo")


#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃              NITIALIZE LOGGING MESSAGE               ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def log_message(message: str, level: str = "info") -> None:
    """Print a formatted message with an emoji prefix."""
    prefixes = {"info": "📍", "success": "📦", "error": "❌"}
    print(f"{prefixes.get(level, '📍')} {message}")


#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃              CACHE Cargo.toml LOCATION               ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
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
        log_message(f"Found Cargo.toml at: {abs_path}", "info")
        return abs_path

    #  ━━━━━━━━━━━━━━━━━━ if Cargo.toml is found ━━━━━━━━━━━━━━━━━━
    current_dir = os.path.abspath(start_dir)
    while current_dir != os.path.dirname(current_dir):
        parent_dir = os.path.dirname(current_dir)
        cargo_path = os.path.join(parent_dir, CARGO_TOML)
        if os.path.exists(cargo_path):
            abs_path = os.path.abspath(cargo_path)
            log_message(f"Found Cargo.toml at: {abs_path}", "info")
            return abs_path
        current_dir = parent_dir
    log_message("Cargo.toml not found in current or parent directories.", "error")
    return None


#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃       SEARCH DEPENDENCIES BLOCK IN Cargo.toml        ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def dependencies_block_find():
    cargo_file = find_cargo_toml()
    if not cargo_file:
        return []

    deps = []
    in_block = False

    with open(cargo_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("[dependencies]") or line.startswith(
                "[dev-dependencies]"
            ):
                in_block = True
                continue
            elif line.startswith("[") and line.endswith("]"):
                in_block = False
                continue

            if in_block:
                dep_name = line.split("=")[0].strip()
                if dep_name:
                    deps.append(dep_name)

    log_message(f"Found dependencies: {deps}", "info")
    return deps


#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃               INSTALLING REQUIREMENTS                ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def install_dependency(dep_name: str) -> None:
    """Install a Rust dependency using cargo add."""
    if not CARGO_PATH:
        log_message("Cargo is not found in PATH.", "error")
        return

    try:
        result = subprocess.run(
            [CARGO_PATH, "add", dep_name], capture_output=True, text=True, check=True
        )
        if result.returncode == 0:
            log_message(f"Successfully added {dep_name}", "success")
        else:
            log_message(
                f"Failed to add {dep_name}: {result.stderr.strip()}",
                "error",
            )
    except Exception as e:
        log_message(f"Exception occurred: {e}", "error")
