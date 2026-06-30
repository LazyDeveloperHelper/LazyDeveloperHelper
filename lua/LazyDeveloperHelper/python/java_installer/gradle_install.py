#!/usr/bin/python3
# -*- coding: utf-8 -*-

from shutil import which as wh
import sys
import subprocess
from pathlib import Path
from logger import log_message

# --- CHECK GRADLE ---
gradle = str(wh("gradle"))


# --- CHECK gradle EXIST ---
def gradle_exists() -> bool:
    if gradle:
        log_message(f"Used Gradle: {gradle}")
        return True
    else:
        log_message("Gradle doesnt exists, install it!", "error")
        return False


# --- FIND GRADLE PROJECT ---
def find_gradle_project() -> Path | None:
    current_dir = Path.cwd()
    for _ in range(10):
        for gradle_file in ["build.gradle.kts", "build.gradle"]:
            if (current_dir / gradle_file).exists():
                log_message(f"Found Gradle project: {
                            current_dir / gradle_file}")
                return current_dir
        if current_dir.parent == current_dir:
            break
        current_dir = current_dir.parent
    return None


# --- ADD DEPENDENCY TO BUILD.GRADLE(.KTS) ---
def add_dependency_to_build(project_dir: Path, lib: str) -> bool:
    build_file = project_dir / "build.gradle.kts"
    if not build_file.exists():
        template = """plugins {
    kotlin("jvm") version "1.9.24"
}

repositories {
    mavenCentral()
}

dependencies {
}
"""
        build_file.write_text(template)
        log_message(f"Created new {
                    build_file.name} with minimal template", "success")

    content = build_file.read_text()

    if "::" in lib:
        _, gav = lib.split("::", 1)
        dep_line = f'    implementation("{gav}")'
        log_msg = gav
        search_dep = gav
    else:
        dep_line = f'    implementation("{lib}:latest.release")'
        log_msg = f"{lib}:latest.release"
        search_dep = f"{lib}:latest.release"

    if any(search_dep in line for line in content.splitlines()):
        log_message(f"'{log_msg}' already present", "info")
        return True

    if 'kotlin("jvm")' not in content:
        if "plugins {" not in content:
            content = 'plugins {\n    kotlin("jvm") version "1.9.24"\n}\n\n' + content
        else:
            content = content.replace(
                "plugins {", 'plugins {\n    kotlin("jvm") version "1.9.24"'
            )
        log_message("Added kotlin('jvm') plugin", "info")

    if "mavenCentral()" not in content:
        if "repositories {" not in content:
            content += "\nrepositories {\n    mavenCentral()\n}\n"
        else:
            content = content.replace(
                "repositories {", "repositories {\n    mavenCentral()"
            )
        log_message("Added mavenCentral()", "info")

    lines = content.splitlines()
    deps_start = next(
        (i for i, line in enumerate(lines) if "dependencies {" in line), None
    )
    if deps_start is None:
        lines.append("")
        lines.append("dependencies {")
        lines.append(dep_line)
        lines.append("}")
    else:
        lines.insert(deps_start + 1, dep_line)

    build_file.write_text("\n".join(lines))
    log_message(f"Added '{log_msg}' → {build_file.name}", "success")
    return True


# --- INSTALLING GRADLE PACKAGE ---
def install_package(lib: str) -> bool:
    project_dir = find_gradle_project()
    if not project_dir:
        log_message("No Gradle project found!", "error")
        return False

    if not add_dependency_to_build(project_dir, lib):
        return False

    try:
        subprocess.run(
            [gradle, "build"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        log_message(f"Successfully downloaded '{lib}'", "success")
        return True
    except subprocess.CalledProcessError:
        log_message("Gradle build failed — check syntax", "error")
        return False


# --- POINT OF ENTER ---
def main() -> None:
    if not gradle_exists():
        return

    if len(sys.argv) < 2:
        log_message("Usage: lib or artifact::group:artifact:version", "error")
        return

    for lib in sys.argv[1:]:
        install_package(lib)


if __name__ == "__main__":
    main()
