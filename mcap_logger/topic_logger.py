import logging

from mcap_protobuf.writer import Writer

from mcap_logger.mcap_handler import McapHandler
from mcap_logger.mcap_logger import Topic


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
