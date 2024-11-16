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
    ) -> None:
        """
        Initializes Topic entity.

        Args:
            name: The name of the topic.
            writer: The MCap file writer with protobuf serialization.
        """
        self._name = name
        self._writer = writer

    def write(self, message: Any) -> None:  # noqa: ANN401
        """
        Writes topic with protobuf message to the log file.

        Args:
            message: The protobuf message.
        """
        timestamp = time.time_ns()
        self._writer.write_message(
            topic=self._name,
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