import logging
import time
from typing import Any

from mcap_protobuf.writer import Writer

from mcap_logger.mcap_handler import McapHandler


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


class TopicLogger:
    def __init__(self, logger_name: str) -> None:
        self._writer = self._fetch_writer_from_logger(logger_name)

    def topic(self, topic_name: str) -> Topic:
        return Topic(topic_name, writer=self._writer)

    @staticmethod
    def _fetch_writer_from_logger(logger_name: str) -> Writer | None:
        for handler in logging.getLogger(logger_name).handlers:
            if isinstance(handler, McapHandler):
                return handler.writer
        return None
