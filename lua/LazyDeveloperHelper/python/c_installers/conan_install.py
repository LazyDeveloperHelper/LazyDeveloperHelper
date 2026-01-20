#!/usr/bin/python3
# -*- coding: utf-8 -*-
import shutil as sh
import sys
from subprocess import run, CalledProcessError
import os
import re
from packaging import version


# --- LOGGING MESSAGE ---
def log_message(message: str, level: str = "info") -> None:
    prefixes = {
        "info": "\U0001f4cd",  # 📍
        "success": "\U0001f4e6",  # 📦
        "error": "\u274c",  # ❌
    }

    print(f"{prefixes.get(level, '\U0001f4cd')} {message}")


# --- VARIABLES ---
CONAN = sh.which("conan")


# --- CHECK CONAN EXIST ---
def conan_exist():
    if CONAN:
        log_message("Conan found!", "success")
        return True
    else:
        log_message("Conan not found, try: pip install conan", "error")
        return False


# -------
# Helpers
# -------
def resolve_package_name(package):
    if "/" in package:
        return package

    log_message(f"Resolving latest version for {package}...", "info")
    result = run(
        ["conan", "search", package, "--remote=conancenter"],
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


def update_conanfile_requires(package_full_name):
    """Update conanfile.txt - KEEP only latest version of each package"""
    lib_short = package_full_name.split("/")[0]  # "fmt"
    full_version = package_full_name.split("/")[-1]  # "12.1.0"

    if not os.path.exists("conanfile.txt"):
        # Create new
        with open("conanfile.txt", "w") as f:
            f.write("[requires]\n")
            f.write(f"{package_full_name}\n\n")
            f.write("[generators]\nCMakeDeps\nCMakeToolchain\n\n")
            f.write("[options]\n*:shared=False\n\n")
            f.write("[imports]\n., * -> ./bin @ keep_path=False\n")
        return True

    requires_lines = []
    with open("conanfile.txt", "r") as f:
        in_requires = False
        for line in f:
            line = line.strip()
            if line == "[requires]":
                in_requires = True
                requires_lines.append(line)
                continue
            if in_requires and line.startswith("["):
                in_requires = False
            if in_requires and line and "/" in line:
                existing_pkg = line.split("/")[0]
                if existing_pkg == lib_short:
                    if version.parse(full_version) > version.parse(line.split("/")[-1]):
                        # Update last line
                        requires_lines[-1] = package_full_name
                        return True
                    return False  # Existing is newer
                requires_lines.append(line)
            elif in_requires:
                requires_lines.append(line)

    # Rewrite with updated requires
    with open("conanfile.txt", "w") as f:
        f.write("[requires]\n")
        for line in requires_lines:
            if line.strip():
                f.write(f"{line}\n")
        f.write("\n[generators]\nCMakeDeps\nCMakeToolchain\n\n")
        f.write("[options]\n*:shared=False\n\n")
        f.write("[imports]\n., * -> ./bin @ keep_path=False\n")

    return True


# --- INSTALLING FUNCTION ---
def install_package(lib: str):
    full_name = resolve_package_name(lib)
    lib_short = full_name.split("/")[0]

    build_dir = f"build_{lib_short.lower()}"
    os.makedirs(build_dir, exist_ok=True)
    # Update conanfile.txt
    updated = update_conanfile_requires(full_name)
    if updated:
        log_message(f"Added {full_name} to conanfile.txt", "info")

    log_message(f"Installing {full_name} → {build_dir}/", "info")

    cmd = [
        "conan",
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
        if os.path.exists(build_dir) and any(os.listdir(build_dir)):
            log_message(f"✅ {lib} successfully installed → {build_dir}/", "success")
            log_message(f"To remove: rm -rf {build_dir}/", "info")
        else:
            log_message(f"⚠️ Installation completed but {build_dir} is empty", "info")
    except CalledProcessError as e:
        error_text = e.stderr.lower() if e.stderr else ""
        if any(x in error_text for x in ["opengl/system", "xorg/system"]):
            log_message(f"{lib} requires system graphics libraries", "info")
            print(
                """Install it! Commands:
Ubuntu/Debian:
    sudo apt install libgl1-mesa-dev libx11-dev libxinerama-dev
    sudo apt install libxcursor-dev libxrandr-dev libxi-dev

Arch/Manjaro:
    sudo pacman -S glu mesa libglvnd libx11 libxinerama
    sudo pacman -S libxcursor libxrandr libxi
"""
            )
        elif "not found" in error_text:
            log_message(f"❌ Package {full_name} not found", "error")
        else:
            log_message(f"❌ Conan failed for {lib}", "error")
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
        log_message("  python conan_installer.py spdlog fmt", "info")
        log_message("  python conan_installer.py zlib boost", "info")
        log_message("  python conan_installer.py spdlog/1.12.0 fmt/9.1.0", "info")
        sys.exit(1)

    for lib in sys.argv[1:]:
        install_package(lib)


# --- POINT OF ENTER ---
if __name__ == "__main__":
    main()
