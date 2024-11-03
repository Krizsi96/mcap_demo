import inspect
import logging
import os
import tempfile
import time
from inspect import Traceback
from pathlib import Path
from typing import Any

from foxglove_schemas_protobuf.Log_pb2 import Log
from google.protobuf.timestamp_pb2 import Timestamp
from mcap_protobuf.writer import Writer

FORMAT = "[{asctime}] [{name}.{funcName}:{lineno}] [{levelname}] {message}"
LOGGER_ROOT = Path(
    os.environ.get(
        "LOGGER_ROOT",
        Path(tempfile.gettempdir()) / "mcap_logger" / "log.mcap",
    ),
)


class Topic:
    def __init__(
        self,
        name: str,
        writer: Writer,
        logger: logging.Logger | None = None,
    ) -> None:
        """
        Initializes Topic entity.

        When logger is not provided the topic won't be logged on the console.

        Args:
            name: The name of the topic.
            writer: The MCap file writer with protobuf serialization.
            logger: The console logger.
        """
        self.name = name
        self.writer = writer
        self.logger = logger

    def write(self, message: Any) -> None:  # noqa: ANN401
        """
        Writes topic with protobuf message to the log file.

        Args:
            message: The protobuf message.
        """
        if self.logger:
            self.logger.debug(f"{self.name} topic:\n{message=}")
        timestamp = int(time.time() * 1_000_000_000)
        self.writer.write_message(
            topic=self.name,
            message=message,
            log_time=timestamp,
            publish_time=timestamp,
        )


class MCAPLogger:
    """
    A class to handle logging activities to an MCap file and to the console.
    """

    def __init__(self, log_file: Path, logger: logging.Logger) -> None:
        """
        Initializes the MCapLogger object.

        Args:
            log_file: The MCap log file to store the logs.
            logger: The console logger.
        """
        self.log_file = log_file.open("wb")
        self.writer = Writer(self.log_file)
        self.log_topic = Topic(name="/log", writer=self.writer)
        self.logger = logger

    def __del__(self) -> None:
        """
        Runs the protobuf writer finish process when the object is deleted.
        """
        self.writer.finish()

    def debug(self, message: str) -> None:
        """
        Logs message with `debug` level.

        Args:
            message: The log message.
        """
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self.logger.debug(message, stacklevel=2)
        self._write_log(level="DEBUG", message=message, traceback=traceback)

    def info(self, message: str) -> None:
        """
        Logs message with `info` level.

        Args:
            message: The log message.
        """
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self.logger.info(message, stacklevel=2)
        self._write_log(level="INFO", message=message, traceback=traceback)

    def warning(self, message: str) -> None:
        """
        Logs message with `warning` level.

        Args:
            message: The log message.
        """
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self.logger.warning(message, stacklevel=2)
        self._write_log(level="WARNING", message=message, traceback=traceback)

    def error(self, message: str) -> None:
        """
        Logs message with `error` level.

        Args:
            message: The log message.
        """
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self.logger.error(message, stacklevel=2)
        self._write_log(level="ERROR", message=message, traceback=traceback)

    def fatal(self, message: str) -> None:
        """
        Logs message with `fatal` level.

        Args:
            message: The log message.
        """
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self.logger.fatal(message, stacklevel=2)
        self._write_log(level="FATAL", message=message, traceback=traceback)

    def _write_log(self, level: str, message: str, traceback: Traceback) -> None:
        """
        Writes the log message to the log file.

        Args:
            level: The log level.
            message: The log message.
            traceback: The traceback of the log call.
        """
        log_message = Log(
            timestamp=Timestamp(nanos=0, seconds=int(time.time())),
            level=level,
            message=message,
            file=f"{traceback.filename}:{traceback.function}()",
            line=traceback.lineno,
        )
        self.log_topic.write(log_message)

    def topic(self, name: str) -> Topic:
        """
        Creates a topic with a name, protobuf writer, and console logger.

        Args:
            name: The name of the topic.

        Returns:
            The created topic.
        """
        return Topic(name, writer=self.writer, logger=self.logger)


def get_logger(
    name: str,
    log_file: Path = LOGGER_ROOT,
    level: int | str | None = None,
) -> MCAPLogger:
    """
    Creates an MCAPLogger entity.

    Args:
        name: The name of the logger.
        log_file: The path to the log file.
        level: The level of the console logger.

    Returns:
        The created MCAPLogger object.
    """
    create_parent_directory_if_not_there(log_file)

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(FORMAT, style="{")
    console_handler.setFormatter(formatter)

    if not level:
        level = os.environ.get("LOG_LEVEL", "WARNING").upper()
    logger = logging.getLogger(name)
    logger.setLevel(level)
    console_handler.setLevel(level)

    logger.addHandler(console_handler)

    return MCAPLogger(log_file, logger)


def create_parent_directory_if_not_there(path: Path) -> None:
    """
    Creates a parent directory if it does not exist.

    Args:
        path: The path of the file with the parent directory.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
