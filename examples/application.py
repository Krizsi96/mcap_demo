import logging
from pathlib import Path

from examples.library import thermostat_monitor
from mcap_logger.mcap_handler import McapHandler


def get_logger(name: str, file: Path) -> logging.Logger:
    logger = logging.getLogger(name)
    mcap_handler = McapHandler(file)
    mcap_handler.setLevel("DEBUG")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel("INFO")

    logger.addHandler(mcap_handler)
    logger.addHandler(stream_handler)
    logger.setLevel("DEBUG")

    library_logger = logging.getLogger("library")
    library_logger.setLevel("DEBUG")
    library_logger.addHandler(stream_handler)
    library_logger.addHandler(mcap_handler)

    return logger


log_file = Path("application.mcap")
log = get_logger("mcap_logger", log_file)


def main():  # noqa: ANN201
    log.info("Hello from mcap-logger-tutorial!")
    thermostat_monitor()


if __name__ == "__main__":
    main()
