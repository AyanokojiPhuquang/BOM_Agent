import sys

from loguru import logger


def format_function(record):
    return (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>\n"
    )


def configure_logging():
    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format=format_function,
        backtrace=True,
        diagnose=True,
    )
