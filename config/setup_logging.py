import logging


def setup_logging(module_name: str, additional_loger: logging = None) -> logging.Logger:
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    log_level = logging.INFO

    # Creating and configuring a logger
    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)

    # Stdout
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)

    # Additional loger
    if additional_loger:
        pass

    return logger
