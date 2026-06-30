#!/usr/bin/python3
# -*- coding: utf-8 -*-
import shutil as sh
import sys
from subprocess import run, CalledProcessError
from logger import log_message
import os
import re
from packaging import version
from typing import List


# --- CONAN location ---
CONAN = str(sh.which("conan"))
if not CONAN:
    log_message("We-woo-wewoo - ur CONAN is NOT installed. Install it!", "error")

# --- CHECK CONAN EXIST ---


def conan_exist():
    if CONAN:
        log_message("Conan found!", "success")
        return True
    log_message("Conan not found, try: pip install conan", "error")
    return False


# -------
# Helpers
# -------
def resolve_package_name(package: str) -> str:
    if "/" in package:
        return package
    log_message(f"Resolving latest version for {package}...", "info")
    result = run(
        [CONAN, "search", package, "--remote=conancenter"],
        capture_output=True,
        text=True,
        check=False,
    )
    versions = []
    for line in result.stdout.splitlines():
        line = line.strip()
        match = re.search(rf"{package}/([^/\s]+)", line)
        if match:
            versions.append(match.group(1))
    if versions:
        latest_version = max(versions, key=version.parse)
        full_name = f"{package}/{latest_version}"
        log_message(f"Resolved version → {full_name}", "success")
        return full_name
    log_message(f"No versions found for {package}", "error")
    return package


def read_requires(conanfile_path: str) -> List[str]:
    if not os.path.exists(conanfile_path):
        return []
    requires = []
    with open(conanfile_path, "r", encoding="utf-8") as f:
        in_requires = False
        for line in f:
            line = line.strip()
            if line == "[requires]":
                in_requires = True
                continue
            if in_requires and line.startswith("["):
                in_requires = False
            if in_requires and line and "/" in line:
                requires.append(line)
    return requires


def add_to_requires(conanfile_path: str, full_name: str):
    if not os.path.exists(conanfile_path):
        ensure_conanfile(conanfile_path)
        return True

    content = []
    has_requires = False
    pkg_short = full_name.split("/")[0]
    already_exists = False

    with open(conanfile_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped == "[requires]":
                has_requires = True
            if has_requires and "/" in stripped and pkg_short in stripped:
                already_exists = True
            content.append(line)

    if already_exists:
        log_message(f"{pkg_short} already in conanfile.txt", "info")
        return False

    with open(conanfile_path, "w", encoding="utf-8") as f:
        in_requires = False
        for line in content:
            stripped = line.strip()
            f.write(line)
            if stripped == "[requires]":
                in_requires = True
            if in_requires and (stripped.startswith("[") or not stripped):
                if not already_exists:
                    f.write(f"{full_name}\n")
                in_requires = False

        if not has_requires:
            f.write("\n[requires]\n")
            f.write(f"{full_name}\n")

    log_message(f"Added {full_name} to conanfile.txt", "success")
    return True


def ensure_conanfile(conanfile_path: str):
    if os.path.exists(conanfile_path):
        return
    template = """[requires]

[generators]
CMakeDeps
CMakeToolchain

[options]
*:shared=False

[imports]
., * -> ./bin @ keep_path=False
"""
    with open(conanfile_path, "w", encoding="utf-8") as f:
        f.write(template)
    log_message(f"Created new {conanfile_path} with base template", "success")


# --- INSTALLING FUNCTION ---
def install_package(lib: str):
    full_name = resolve_package_name(lib)
    if not full_name:
        return

    conanfile_path = "conanfile.txt"
    ensure_conanfile(conanfile_path)

    if add_to_requires(conanfile_path, full_name):
        log_message(f"Updated conanfile.txt with {full_name}", "info")

    build_dir = f"build_{lib.lower()}"
    os.makedirs(build_dir, exist_ok=True)

    log_message(f"Running conan install for {full_name} → {build_dir}/", "info")
    cmd = [
        CONAN,
        "install",
        ".",
        "--build=missing",
        "-v",
        "--output-folder",
        build_dir,
        "--update",
    ]
    try:
        run(cmd, check=True, text=True, capture_output=True)
        log_message(f"{lib} successfully installed → {build_dir}/", "success")
        log_message(f"To remove: rm -rf {build_dir}/", "info")
    except CalledProcessError as e:
        log_message(f"Conan failed for {lib}", "error")
        print("Error output:")
        print(e.stderr if e.stderr else e.stdout)


# --- MAIN FUNCTION ---
def main() -> None:
    if not conan_exist():
        sys.exit(1)
    if len(sys.argv) < 2:
        log_message(
            "Usage: python conan_installer.py <package1> <package2> ...", "info"
        )
        log_message("Examples:", "info")

        log_message("Examples:", "info")
        log_message(" python conan_installer.py spdlog fmt", "info")
        log_message(" python conan_installer.py zlib/1.2.13 boost/1.85.0", "info")
        sys.exit(1)
    for lib in sys.argv[1:]:
        install_package(lib)


if __name__ == "__main__":
    main()
