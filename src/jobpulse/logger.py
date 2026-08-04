import logging


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

    if not logger.handlers:
        logger.addHandler(handler)