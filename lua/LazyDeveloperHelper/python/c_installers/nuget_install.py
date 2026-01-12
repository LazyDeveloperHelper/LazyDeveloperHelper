# -*- coding: utf-8 -*-
import shutil as sh
import sys
from subprocess import run, CalledProcessError


# --- LOGGING MESSAGE ---
def log_message(message: str, level: str = "info") -> None:
    prefixes = {
        "info": "\U0001f4cd",  # 📍
        "success": "\U0001f4e6",  # 📦
        "error": "\u274c",  # ❌
    }

    print(f"{prefixes.get(level, '\U0001f4cd')} {message}")


# --- CHECK NuGet is exist ---
def nuget_exist() -> bool:
    dotnet_path = sh.which("dotnet")
    if dotnet_path:
        log_message("Dotnet exists!", "info")
        return True
    else:
        log_message("Dotnet isnt exists, try install it!", "critical")
        return False


# --- INSTALLLING LIBS ---
def install_lib(lib_name: str):
    message_for_run = ["dotnet", "add", "package", lib_name]
    try:
        result = run(message_for_run, check=True, capture_output=True, text=True)
        log_message(f"NuGet install output:\n{result.stdout}", "info")
    except CalledProcessError as err:
        log_message(f"Dotnet install failed:\n{err.stderr}", "error")


# --- POINT OF ENTER ---
if __name__ == "__main__":
    if not nuget_exist():
        sys.exit(1)

    for lib in sys.argv[1:]:
        install_lib(lib)
