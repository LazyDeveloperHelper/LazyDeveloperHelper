#!/usr/bin/python3

from subprocess import run, CalledProcessError, PIPE
from shutil import which
import sys
from logger import logger


# -- VARIABLES --
GEM_PATH = which("gem")


# --- CHECK IS GEM EXIST ---
def check_gem():
    """Check if the 'gem' command is available on the system."""
    if GEM_PATH:
        logger("✅ Gem is found!", "success")
    else:
        logger(
            "❌ Gem not found, try to install by: `sudo apt install ruby-rubygems`",
            "error",
        )
        sys.exit(1)


# --- INSTALL LIBRARIES BY 'gem install {}' ---
def install_gem(lib_name: str):
    """Install a Ruby gem using the 'gem install' command."""
    if not GEM_PATH:
        logger("Gem is not installed.", "error")
        sys.exit(1)
    try:
        result = run(
            [GEM_PATH, "install", lib_name, "--user-install"],
            check=True,
            text=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        if "Successfully installed" in result.stdout:
            logger(f"Successfully installed {lib_name}", "success")
    except CalledProcessError as e:
        logger(f"Failed to install {lib_name}: {e.stderr}", "error")
        sys.exit(1)


# --- POINT OF ENTER ---
def main() -> None:
    if len(sys.argv) < 2:
        print("Provide at least one npm package name")
        return
    for lib in sys.argv[1:]:
        install_gem(lib)


if __name__ == "__main__":
    main()
