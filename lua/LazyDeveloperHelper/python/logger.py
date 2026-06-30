#!/usr/bin/env python3

from __future__ import annotations

import logging
from pathlib import Path


_PREFIXES = {
    "info": "\U0001f4cd",  # 📍
    "success": "\U0001f4e6",  # 📦
    "error": "\u274c",  # ❌
}

_LOGGERS: dict[str, logging.Logger] = {}


def _get_logger(filename: str) -> logging.Logger:
    logger = _LOGGERS.get(filename)
    if logger is not None:
        return logger

    logger = logging.getLogger(f"LazyDeveloperHelper.{filename}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.FileHandler(Path(filename), mode="a", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(message)s"))
        handler.terminator = ""
        logger.addHandler(handler)

    _LOGGERS[filename] = logger
    return logger


def log_message(message: str, level: str = "info", filename: str = "app.log") -> None:
    prefix = _PREFIXES.get(level, _PREFIXES["info"])
    _get_logger(filename).info("%s %s", prefix, message)
