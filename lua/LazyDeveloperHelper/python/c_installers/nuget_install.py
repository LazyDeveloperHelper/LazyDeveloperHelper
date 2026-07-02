# -*- coding: utf-8 -*-
import shutil as sh
import sys
from subprocess import run, CalledProcessError
from logger import logger
#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


dotnet_path = sh.which("dotnet")


#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def nuget_exist() -> bool:
    if dotnet_path:
        logger("Dotnet exists!", "info")
        return True
    else:
        logger("Dotnet isnt exists, try install it!", "critical")
        return False


# --- INSTALLLING LIBS ---
def install_lib(lib_name: str):
    message_for_run = ["dotnet", "add", "package", lib_name]
    try:
        result = run(message_for_run, check=True, capture_output=True, text=True)
        logger(f"NuGet install output:\n{result.stdout}", "info")
    except CalledProcessError as err:
        logger(f"Dotnet install failed:\n{err.stderr}", "error")


# --- POINT OF ENTER ---
if __name__ == "__main__":
    if not nuget_exist():
        sys.exit(1)

    for lib in sys.argv[1:]:
        install_lib(lib)
