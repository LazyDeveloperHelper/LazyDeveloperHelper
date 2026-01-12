#!/usr/bin/python3
# -*- coding: utf-8 -*-
import shutil as sh
import sys
from subprocess import run, CalledProcessError
import os
import re


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
    """
    If only name is given (e.g. "spdlog"), resolve latest version from ConanCenter.
    If full name+version (e.g. "spdlog/1.14.1") — return as-is.
    """
    if "/" in package:
        return package

    log_message(f"Resolving latest version for {package}...", "info")
    try:
        result = run(
            ["conan", "search", f"{package}/*", "--remote=conancenter"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            log_message(f"Package {package} not found on ConanCenter", "error")
            return package

        versions = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if line and "/" in line and line.startswith(package + "/"):
                version_match = re.match(rf"{package}/([^/\s]+)", line)
                if version_match:
                    version = version_match.group(1)
                    versions.append(version)

        if versions:
            latest_version = sorted(versions)[-1]
            full_name = f"{package}/{latest_version}"
            log_message(f"Resolved version → {full_name}", "success")
            return full_name
        else:
            log_message(f"No versions found for {package}", "error")
            return package

    except Exception as e:
        log_message(f"Failed to resolve version: {e}", "error")
        return package


def update_conanfile_requires(package_full_name):
    """Update conanfile.txt with the package requirement"""
    lib_short = package_full_name.split("/")[0]
    if not os.path.exists("conanfile.txt"):
        with open("conanfile.txt", "w") as f:
            f.write("[requires]\n")
            f.write(f"{package_full_name}\n\n")
            f.write("[generators]\nCMakeDeps\nCMakeToolchain\n\n")
            f.write("[options]\n*:shared=False\n\n")
            f.write("[imports]\n., * -> ./bin @ keep_path=False\n")
        return True

    with open("conanfile.txt", "r") as f:
        content = f.read()
        lines = content.splitlines()

    package_exists = any(
        line.strip().startswith(f"{lib_short}/")
        for line in lines
        if line.strip() and not line.startswith("[")
    )

    if not package_exists:
        new_lines = []
        requires_section_found = False
        requires_content_added = False
        for line in lines:
            new_lines.append(line)
            if line.strip() == "[requires]" and not requires_section_found:
                requires_section_found = True
            elif requires_section_found and not requires_content_added:
                if line.strip() == "" or line.strip().startswith("["):
                    new_lines.append(package_full_name)
                    requires_content_added = True
        if requires_section_found and not requires_content_added:
            new_lines.append(package_full_name)

        if not requires_section_found:
            new_lines.append("[requires]")
            new_lines.append(package_full_name)
            new_lines.append("")

        with open("conanfile.txt", "w") as f:
            f.write("\n".join(new_lines) + "\n")
        return True
    return False


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
