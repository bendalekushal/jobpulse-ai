import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


def configure_logging():
    """
    Configure the application's root logger.
    Call this only once from the application's entry point.
    """

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | Line:%(lineno)d | %(message)s"
    )

    handler.setFormatter(formatter)

    log_dir = Path("logs")

    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "app.log"

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=500,
        backupCount=3,
    )
    file_handler.setFormatter(formatter)

    if not logger.handlers:
            logger.addHandler(handler)
            logger.addHandler(file_handler)
        