import logging
import time
from pathlib import Path
from typing import TYPE_CHECKING

from foxglove_schemas_protobuf.Log_pb2 import Log
from google.protobuf.timestamp_pb2 import Timestamp
from mcap_protobuf.writer import Writer

if TYPE_CHECKING:
    from io import TextIOWrapper


class McapHandler(logging.Handler):
    """
    A handler class which writes log messages
    to MCAP files using ProtoBuf serialization.
    """

    def __init__(self, file: Path) -> None:
        """
        Open the specified file and use it as the stream for logging.

        If the file already exists, it will be overwritten.

        If the parent directory does not exist, it will be created.

        Args:
            file: The MCAP file to store the logs.
        """
        super().__init__()
        self._file: Path | TextIOWrapper = file
        self.writer: None | Writer = None
        self._open()

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a record.

        The record will be emitted under the `/log` topic.

        Args:
            record: The record to emit into the log file.
        """
        time_sec, time_ns = _split_time(record.created)

        log_message = Log(
            timestamp=Timestamp(nanos=time_ns, seconds=time_sec),
            level=record.levelname,
            message=record.getMessage(),
            name=record.module,
            file=record.filename,
            line=record.lineno,
        )

        self.writer.write_message(
            topic="/log",
            message=log_message,
            log_time=int(record.created * 1_000_000_000),
            publish_time=time.time_ns(),
        )

    def close(self) -> None:
        """
        Close the file.
        """
        self.writer.finish()
        self._file.close()
        super().close()

    def _open(self) -> None:
        """
        Open the log file and initialize the ProtoBuf writer.

        If the parent directory does not exist, it will be created.
        """
        if self.writer is None:
            self._file.parent.mkdir(parents=True, exist_ok=True)
            self._file = self._file.open("wb")
            self.writer = Writer(self._file)


def _split_time(time_to_split: float) -> (int, int):
    """
    Split the time into the `seconds` part and `nanos` part.

    Args:
        time_to_split: The time in seconds to split.

    Returns:
        The `seconds` part and `nanos` part as tuple of integers.
    """
    time_seconds = int(time_to_split)
    time_nanos = int((time_to_split - time_seconds) * 1_000_000_000)
    return time_seconds, time_nanos
