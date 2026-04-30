#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from subprocess import run, CalledProcessError, PIPE
from shutil import which
import sys
from pathlib import Path

go_path = which("go")


def log_message(message: str, level: str = "info") -> None:
    prefixes = {
        "info": "\U0001f4cd",
        "success": "\U0001f4e6",
        "error": "\u274c",
    }
    print(f"{prefixes.get(level, '\U0001f4cd')} {message}")


def check_go_installed() -> bool:
    if not go_path:
        log_message("Go is not installed or not in PATH.", "error")
        return False
    log_message(f"Using Go: {go_path}")
    return True


POPULAR_PACKAGES = {
    "echo": "github.com/labstack/echo/v4",
    "gin": "github.com/gin-gonic/gin",
    "fiber": "github.com/gofiber/fiber/v2",
    "chi": "github.com/go-chi/chi/v5",
    "mux": "github.com/gorilla/mux",
    "beego": "github.com/beego/beego/v2",
    "iris": "github.com/kataras/iris/v12",
}


def normalize_package(lib: str) -> str:
    if lib.startswith("github.com/"):
        return lib
    if "@" in lib:
        name, version = lib.split("@", 1)
        name = name.lower()
        base_path = POPULAR_PACKAGES.get(name, f"github.com/{name}/{name}")
        return f"{base_path}@{version}"
    name = lib.lower()
    base_path = POPULAR_PACKAGES.get(name, f"github.com/{name}/{name}")
    return f"{base_path}@latest"


def install_lib(lib: str) -> None:
    if not check_go_installed():
        return
    package = normalize_package(lib)
    log_message(f"Installing Go package: {package} ...", "info")
    project_dir = Path.cwd()
    if not (project_dir / "go.mod").exists():
        try:
            run([str(go_path), "mod", "init", "myproject"], check=True, cwd=project_dir)
            log_message("Created new go.mod", "success")
        except Exception as e:
            log_message(f"Failed to init go.mod: {e}", "error")
            return
    try:
        result = run(
            [str(go_path), "get", package],
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            check=True,
            cwd=project_dir,
        )
        log_message(f"✅ {lib} added to go.mod successfully!", "success")
        if result.stdout:
            print(result.stdout)
    except CalledProcessError as e:
        log_message(f"❌ Failed to add {lib}", "error")
        if e.stdout:
            print("🔻 stdout:\n", e.stdout)
        if e.stderr:
            print("stderr:\n", e.stderr)
        print("Return code:", e.returncode)


def main() -> None:
    if len(sys.argv) < 2:
        log_message(
            "Usage: :LazyDevInstall echo or Echo@v4.12.0 or github.com/labstack/echo/v4@latest",
            "error",
        )
        return
    for lib in sys.argv[1:]:
        install_lib(lib)


if __name__ == "__main__":
    main()
