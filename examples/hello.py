import logging
from pathlib import Path

from mcap_logger.mcap_handler import McapHandler


def main():  # noqa: ANN201
    logger = logging.getLogger("mcap_logger")
    log_file = Path("hello.mcap")
    mcap_handler = McapHandler(log_file)
    mcap_handler.setLevel("DEBUG")

    logger.addHandler(mcap_handler)
    logger.setLevel("DEBUG")

    logger.info("Hello from mcap-logger-tutorial!")


if __name__ == "__main__":
    main()
