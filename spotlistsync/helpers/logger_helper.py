import logging


def get_logger(module_name, logging_level=logging.INFO):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging_level)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger
