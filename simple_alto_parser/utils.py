import logging

LOGGER = None

def get_logger():
    """This function returns a logger instance for the package."""

    global LOGGER

    if LOGGER is not None:
        return LOGGER

    LOGGER = logging.getLogger("simple_alto_parser")
    LOGGER.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    LOGGER.addHandler(ch)

    ch2 = logging.FileHandler('alto_parser.log')
    ch2.setLevel(logging.DEBUG)
    ch2.setFormatter(formatter)
    LOGGER.addHandler(ch2)

    return LOGGER
