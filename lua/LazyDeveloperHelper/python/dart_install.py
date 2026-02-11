# --- IMPORTS ---
from logger import log_message as logger
from subprocess import run, CalledProcessError
from shutil import which
from pathlib import Path


# --- dart LOCATION ---
dart = which("dart")
if dart:
    logger("Dart found successfully, continuing...", "success")
else:
    logger("Dart not found, install it in PATH!", "error")


# --- ENSURE pubspec.yaml ---
def ensure_pubspec_yaml():
    pubspec_path = Path.cwd() / "pubspec.yaml"
    if not pubspec_path.exists():
        logger("pubspec.yaml not found! Creating minimal one...", "info")
        minimal_content = """
name: lazydev_test_project
description: Auto-created for LazyDeveloperHelper installer test
version: 1.0.0

environment:
  sdk: '>=3.0.0 <4.0.0'
"""
        pubspec_path.write_text(minimal_content.strip())
        logger("Created pubspec.yaml")
    else:
        logger("pubspec.yaml already exists")


# --- INSTALL LIB ---
def install_package(package: str):
    ensure_pubspec_yaml()
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


install_package("googleapis")
