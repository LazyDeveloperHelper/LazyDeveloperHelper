#!/usr/bin/env python3

# --- IMPORTS ---
from logger import logger
from subprocess import run, CalledProcessError
from shutil import which
import pathlib
import sys
import re
import os

# --- dart LOCATION ---
dart = which("dart")
if dart:
    logger("Dart found successfully, continuing...", "success")
else:
    logger("Dart not found, install it in PATH!", "error")


# --- HELPERS ---
def ensure_pubspec_yaml():
    pubspec_path = pathlib.Path.cwd() / "pubspec.yaml"
    if not pubspec_path.exists():
        logger("pubspec.yaml not found! Creating minimal one...", "info")
        minimal_content = """
name: LazyDeveloperHelper_Minimal_Config
description: Auto-created for LazyDeveloperHelper[Dart] installer
version: 1.0.0

environment:
  sdk: '>=3.0.0 <4.0.0'
"""
        pubspec_path.write_text(minimal_content.strip())
        logger("Created pubspec.yaml")
    else:
        logger("pubspec.yaml already exists")


def is_package_installed(package: str) -> bool:
    pubspec_path = os.path.join(os.getcwd(), "pubspec.yaml")
    if not os.path.exists(pubspec_path):
        return False
    with open(pubspec_path, "r") as f:
        content = f.read()
    # Check if package name appears in dependencies section
    return bool(re.search(rf"^\s+{re.escape(package)}:", content, re.MULTILINE))


# --- INSTALL LIB ---
def install_package(package: str):
    ensure_pubspec_yaml()
    if is_package_installed(package):
        logger(f"{package} is already installed, skipping", "success")
        return
    cmd = [dart, "pub", "add", package]
    logger(f"Installing {package}...")

    try:
        result = run(cmd, check=True, text=True, capture_output=True)
        logger(f"{package} installed successfully", "success")
        logger(result.stdout.strip() or "No output")

    except CalledProcessError as e:
        logger(f"Failed to install {package}")
        logger(f"Command: {' '.join(e.cmd)}")
        if e.stderr:
            logger(f"STDERR: {e.stderr.strip()}", "error")
        if e.stdout:
            logger(f"STDOUT: {e.stdout.strip()}")
        raise

    except FileNotFoundError:
        logger("Dart not found in PATH", "error")
        raise


# --- MAIN ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        pkg = sys.argv[1]
        install_package(pkg)
    else:
        logger("Provide any package!", "error")
