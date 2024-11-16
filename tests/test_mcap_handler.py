import logging
import time
from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock

import pytest
from foxglove_schemas_protobuf.Log_pb2 import Log
from freezegun import freeze_time
from google.protobuf.timestamp_pb2 import Timestamp
from mcap.reader import make_reader
from mcap_protobuf.decoder import DecoderFactory

from mcap_logger.mcap_handler import McapHandler


@mock.patch("mcap_logger.mcap_handler.Writer")
@mock.patch("mcap_logger.mcap_handler.Path")
def test_mcap_handler_init(mocked_log_file, mocked_mcap_writer_constructor):
    # Given
    mcap_writer = MagicMock()
    mocked_mcap_writer_constructor.return_value = mcap_writer
    opened_log_file = MagicMock()
    mocked_log_file.open.return_value = opened_log_file

    # When
    handler = McapHandler(mocked_log_file)

    # Then
    mocked_log_file.open.assert_called_once_with("wb")
    mocked_mcap_writer_constructor.assert_called_once_with(opened_log_file)
    assert handler._file == opened_log_file
    assert handler.writer == mcap_writer


@pytest.fixture
@mock.patch("mcap_logger.mcap_handler.Writer")
@mock.patch("mcap_logger.mcap_handler.Path")
def create_mcap_handler(mocked_log_file, mocked_mcap_writer_constructor):
    mocked_mcap_writer = MagicMock()
    mocked_mcap_writer_constructor.return_value = mocked_mcap_writer
    opened_log_file = MagicMock()
    mocked_log_file.open.return_value = opened_log_file

    mcap_handler = McapHandler(mocked_log_file)

    return {
        "mcap_handler": mcap_handler,
        "mocked_mcap_writer": mocked_mcap_writer,
        "mocked_log_file": mocked_log_file,
        "opened_log_file": opened_log_file,
    }


def test_mcap_handler_only_opens_the_log_file_once(create_mcap_handler):
    # Given
    handler = create_mcap_handler["mcap_handler"]
    mocked_log_file = create_mcap_handler["mocked_log_file"]

    # When
    handler._open()
    handler._open()

    # Then
    mocked_log_file.open.assert_called_once()


def test_mcap_handler_log_file_closing(create_mcap_handler):
    # Given
    handler = create_mcap_handler["mcap_handler"]
    opened_log_file = create_mcap_handler["opened_log_file"]
    mocked_mcap_writer = create_mcap_handler["mocked_mcap_writer"]

    # When
    handler.close()

    # Then
    opened_log_file.close.assert_called_once()
    mocked_mcap_writer.finish.assert_called_once()


@freeze_time("2022-02-03 14:53:23.986")
@mock.patch("mcap_logger.mcap_handler.Log")
def test_mcap_handler_emit_writes_protobuf_log(
    mocked_log_constructor, create_mcap_handler
):
    # Given
    handler = create_mcap_handler["mcap_handler"]
    mocked_mcap_writer = create_mcap_handler["mocked_mcap_writer"]

    full_time = time.time()
    time_sec = int(full_time)
    time_nano = int((full_time - time_sec) * 1_000_000_000)

    record = MagicMock()
    record.levelname = "INFO"
    record.filename = "test.py"
    record.module = "test"
    record.lineno = 1
    record.getMessage.return_value = "test message"
    record.created = full_time

    mocked_log_message = MagicMock()
    mocked_log_constructor.return_value = mocked_log_message

    # When
    handler.emit(record)

    # Then
    mocked_log_constructor.assert_called_once_with(
        timestamp=Timestamp(nanos=time_nano, seconds=time_sec),
        level=record.levelname,
        name=record.module,
        message=record.getMessage(),
        file=record.filename,
        line=record.lineno,
    )

    mocked_mcap_writer.write_message.assert_called_once_with(
        topic="/log",
        message=mocked_log_message,
        log_time=int(full_time * 1_000_000_000),
        publish_time=int(full_time * 1_000_000_000),
    )


def test_mcap_handler_log_creation(tmpdir):
    # Given
    file = Path(str(tmpdir)) / "test.mcap"
    handler = McapHandler(file)
    record = logging.LogRecord(
        name="name",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="test message",
        args=None,
        exc_info=None,
    )

    # When
    handler.emit(record)
    handler.close()

    # Then
    assert file.exists()
    with file.open("rb") as f:
        reader = make_reader(f, decoder_factories=[DecoderFactory()])
        messages = list(reader.iter_decoded_messages())

        assert len(messages) == 1

        for schema, channel, message, proto_msg in messages:
            assert schema.name == "foxglove.Log"
            assert schema.encoding == "protobuf"
            assert channel.topic == "/log"

            assert proto_msg.name == "test"
            assert proto_msg.level == Log.Level.INFO
            assert proto_msg.message == "test message"
            assert proto_msg.file == "test.py"
            assert proto_msg.line == 1
