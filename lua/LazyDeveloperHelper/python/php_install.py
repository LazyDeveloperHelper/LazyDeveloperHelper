#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from shutil import which
from logger import log_message as logger
from subprocess import run


COMPOSER_PATH = which("composer")
if not COMPOSER_PATH:
    logger("Composer CLI are NOT found! Install it!", "error")
else:
    logger("Composer is here, nice", "success")
#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def install_libs(deps: dict[str, str]):
    cmd = f"{COMPOSER_PATH} require {deps['author']}/{deps['dep_name']}"
    result = run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger(
            f"Failed to install {deps['author']}/{deps['dep_name']}: {result.stderr}",
            "error",
            filename="php_install.py",
        )
    else:
        # if "Already installed" in result.stdout:
        logger(
            f"Installed {deps['author']}/{deps['dep_name']}",
            "success",
            filename="php_install.py",
        )
