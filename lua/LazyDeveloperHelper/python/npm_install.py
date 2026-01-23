#!/usr/bin/env python3
from subprocess import run, CalledProcessError, PIPE
from shutil import which
import sys
from logger import log_message

# --- npm PATH ---
npm_path = which("npm")


# --- CHECKING npm INSTALLED
def check_npm_installed() -> bool:
    if not npm_path:
        log_message("npm is not installed or not found in PATH.", "error")
        return False
    return True


# --- VALIDATE LIB NAME ---
def validate_library_name(lib: str) -> bool:
    if not lib or any(c in lib for c in '<>|&;"'):
        log_message(f"Invalid package name: {lib}", "error")
        return False
    return True


# --- INSTALLING LIBS
def install_npm(lib: str) -> None:
    """Install an npm package if not already present."""
    if not check_npm_installed():
        return
    if not validate_library_name(lib):
        return

    log_message(f"Installing npm package: {lib} ...", "info")
    try:
        result = run(
            [str(npm_path), "list", lib],
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            check=True,
            capture_output=True,
        )
        # If list contains package name — treat as installed
        if lib in (result.stdout or ""):
            log_message(f"{lib} already installed", "success")
            return
    except Exception:
        # If npm list itself fails unexpectedly, continue to attempt install
        pass

    # Try installing - keep check=True to raise CalledProcessError on failure
    try:
        result = run(
            [str(npm_path), "install", lib.lower(), "--no-save"],
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            check=True,
        )
        print(f"✅ {lib} installed successfully")
    except CalledProcessError as e:
        print(f"❌ Failed to install {lib}")
        print("🔻 stdout:\n", e.stdout)
        print("🔻 stderr:\n", e.stderr)
        print("🔚 Return code:", e.returncode)


# --- POINT OF ENTER ---
def main() -> None:
    if len(sys.argv) < 2:
        print("Provide at least one npm package name")
        return
    for lib in sys.argv[1:]:
        install_npm(lib)


if __name__ == "__main__":
    main()
