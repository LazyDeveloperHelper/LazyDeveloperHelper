#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
import shutil
from logger import logger


def find_vcpkg():
    """Find vcpkg executable cross-platform."""
    vcpkg_path = shutil.which("vcpkg")
    if not vcpkg_path:
        logger("vcpkg not found in PATH. Install it first!", "critical")
        print(
            "Linux: \ngit clone https://github.com/Microsoft/vcpkg\n"
            "./vcpkg/bootstrap-vcpkg.sh"
        )
        sys.exit(1)

    logger(f"Found vcpkg: {vcpkg_path}", "info")
    return vcpkg_path


# --- INSTALL PACKAGE BY vcpkg install ---
def install_package(pkg: str):
    vcpkg_path = find_vcpkg()
    command = [vcpkg_path, "install", pkg]
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        logger(f"Installing: {pkg}")
        if "All requested installations completed successfully" in result.stdout:
            logger(f"Successfully installed {pkg}!")
            return True
    except subprocess.CalledProcessError as e:
        logger(f"Failed: {e.stderr}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger("Usage: :LazyDevInstall {package} (NeoVim Version)")
        logger("Or (Directly): python3 vcpkg_install.py {package} (CLI Version)")
        sys.exit(1)
    package = sys.argv[1]
    install_package(package)
