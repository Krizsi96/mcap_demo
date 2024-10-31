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
        self.name = name
        self.writer = writer
        self.logger = logger

    def write(self, message: Any) -> None:  # noqa: ANN401
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
    def __init__(self, log_file: Path, logger: logging.Logger) -> None:
        self.log_file = log_file.open("wb")
        self.writer = Writer(self.log_file)
        self.log_topic = Topic(name="/log", writer=self.writer)
        self.logger = logger

    def __del__(self) -> None:
        self.writer.finish()

    def debug(self, message: str) -> None:
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self.logger.debug(message, stacklevel=2)
        self._write_log(level="DEBUG", message=message, traceback=traceback)

    def info(self, message: str) -> None:
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self.logger.info(message, stacklevel=2)
        self._write_log(level="INFO", message=message, traceback=traceback)

    def warning(self, message: str) -> None:
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self.logger.warning(message, stacklevel=2)
        self._write_log(level="WARNING", message=message, traceback=traceback)

    def error(self, message: str) -> None:
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self.logger.error(message, stacklevel=2)
        self._write_log(level="ERROR", message=message, traceback=traceback)

    def fatal(self, message: str) -> None:
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self.logger.fatal(message, stacklevel=2)
        self._write_log(level="FATAL", message=message, traceback=traceback)

    def _write_log(self, level: str, message: str, traceback: Traceback) -> None:
        log_message = Log(
            timestamp=Timestamp(nanos=0, seconds=int(time.time())),
            level=level,
            message=message,
            file=f"{traceback.filename}:{traceback.function}()",
            line=traceback.lineno,
        )
        self.log_topic.write(log_message)

    def topic(self, name: str) -> Topic:
        return Topic(name, writer=self.writer, logger=self.logger)


def get_logger(
    name: str,
    log_file: Path = LOGGER_ROOT,
    level: int | str | None = None,
) -> MCAPLogger:
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
    path.parent.mkdir(parents=True, exist_ok=True)
