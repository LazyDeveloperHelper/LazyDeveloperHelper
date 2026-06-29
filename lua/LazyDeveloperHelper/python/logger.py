# -*- coding: utf-8 -*-


# --- LOGGING MESSAGE ---
def log_message(message: str, level: str = "info", filename: str = "app.log") -> None:
    prefixes = {
        "info": "\U0001f4cd",  # 📍
        "success": "\U0001f4e6",  # 📦
        "error": "\u274c",  # ❌
    }

    log_string = f"{prefixes.get(level, '\U0001f4cd')} {message}"
    with open(file=filename, mode="a") as file:
        file.write(log_string)
