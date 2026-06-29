#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
import shutil


# --- LOGGING MESSAGE ---
def log_message(message: str, level: str = "info", filename: str = "app.log") -> None:
    prefixes = {
        "info": "\U0001f4cd",  # 📍
        "success": "\U0001f4e6",  # 📦
        "error": "\u274c",
    }  # ❌
    log_string = f"{prefixes.get(level, '\U0001f4cd')} {message}"
    with open(file=filename, mode="a") as file:
        file.write(log_string)


def find_vcpkg():
    """Find vcpkg executable cross-platform."""
    vcpkg_path = shutil.which("vcpkg")
    if not vcpkg_path:
        log_message("vcpkg not found in PATH. Install it first!", "critical")
        print(
            "Linux: \ngit clone https://github.com/Microsoft/vcpkg\n"
            "./vcpkg/bootstrap-vcpkg.sh"
        )
        sys.exit(1)

    log_message(f"Found vcpkg: {vcpkg_path}", "info")
    return vcpkg_path


# --- INSTALL PACKAGE BY vcpkg install ---
def install_package(pkg: str):
    vcpkg_path = find_vcpkg()
    command = [vcpkg_path, "install", pkg]
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        log_message(f"Installing: {pkg}")
        if "All requested installations completed successfully" in result.stdout:
            log_message(f"Successfully installed {pkg}!")
            return True
    except subprocess.CalledProcessError as e:
        log_message(f"Failed: {e.stderr}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        log_message("Usage: :LazyDevInstall {package} (NeoVim Version)")
        log_message("Or (Directly): python3 vcpkg_install.py {package} (CLI Version)")
        sys.exit(1)
    package = sys.argv[1]
    install_package(package)
