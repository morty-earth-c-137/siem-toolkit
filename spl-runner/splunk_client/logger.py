"""
logger.py
---------
Configures structured console logging for the entire application.
"""

import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configures root logger to write structured output to stdout.

    Args:
        level (int): Logging level. Defaults to logging.INFO.
    """
    log_format = "[%(asctime)s] [%(levelname)-8s] [%(name)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    root_logger = logging.getLogger()
    if root_logger.handlers:
        root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))

    root_logger.setLevel(level)
    root_logger.addHandler(handler)

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
