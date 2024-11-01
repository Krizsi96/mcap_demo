import gc
import time
from contextlib import contextmanager
from unittest import mock
from unittest.mock import MagicMock

import pytest
from foxglove_schemas_protobuf.Log_pb2 import Log
from freezegun import freeze_time
from google.protobuf.timestamp_pb2 import Timestamp

from mcap_logger.mcap_logger import MCAPLogger


@mock.patch("mcap_logger.mcap_logger.Topic")
@mock.patch("mcap_logger.mcap_logger.Writer")
@mock.patch("mcap_logger.mcap_logger.logging.Logger")
@mock.patch("mcap_logger.mcap_logger.Path")
def test_mcap_logger_init(mocked_log_file, mocked_logger, mocked_writer, mocked_topic):
    # When
    mcap_logger = MCAPLogger(mocked_log_file, mocked_logger)

    # Then
    mocked_log_file.open.assert_called_once_with("wb")
    mocked_writer.assert_called_once_with(mcap_logger.log_file)
    mocked_topic.assert_called_once_with(name="/log", writer=mcap_logger.writer)
    assert mcap_logger.logger == mocked_logger


@mock.patch("mcap_logger.mcap_logger.Writer")
@mock.patch("mcap_logger.mcap_logger.logging.Logger")
@mock.patch("mcap_logger.mcap_logger.Path")
def test_mcap_logger_deletion(
    mocked_log_file, mocked_logger, mocked_writer_constructor
):
    # Given
    writer = MagicMock()
    mocked_writer_constructor.return_value = writer
    mcap_logger = MCAPLogger(mocked_log_file, mocked_logger)

    # When
    del mcap_logger
    gc.collect()

    # Then
    writer.finish.assert_called_once()


@pytest.fixture
@mock.patch("mcap_logger.mcap_logger.Topic")
@mock.patch("mcap_logger.mcap_logger.Writer")
@mock.patch("mcap_logger.mcap_logger.logging.Logger")
@mock.patch("mcap_logger.mcap_logger.Path")
def create_mcap_logger(
    mocked_log_file, mocked_logger, mocked_writer_constructor, mocked_topic_constructor
):
    mocked_writer = MagicMock()
    mocked_writer_constructor.return_value = mocked_writer
    opened_log_file = MagicMock()
    mocked_log_file.open.return_value = opened_log_file
    mocked_topic = MagicMock()
    mocked_topic_constructor.return_value = mocked_topic

    mcap_logger = MCAPLogger(mocked_log_file, mocked_logger)

    return {
        "mcap_logger": mcap_logger,
        "opened_log_file": opened_log_file,
        "mocked_topic": mocked_topic,
        "mocked_writer": mocked_writer,
        "mocked_logger": mocked_logger,
    }


@contextmanager
def frame_info_mock(file_name: str, function_name: str, line_number: int):
    with mock.patch(
        "mcap_logger.mcap_logger.inspect.getframeinfo"
    ) as mocked_getframeinfo:
        mocked_frame_info = MagicMock()
        mocked_frame_info.filename = file_name
        mocked_frame_info.function = function_name
        mocked_frame_info.lineno = line_number
        mocked_getframeinfo.return_value = mocked_frame_info

        yield mocked_getframeinfo


@freeze_time("2022-02-03 14:53:23.986")
def test_debug_logging(create_mcap_logger):
    # Given
    mcap_logger = create_mcap_logger["mcap_logger"]
    mocked_logger = create_mcap_logger["mocked_logger"]
    mocked_topic = create_mcap_logger["mocked_topic"]
    message = "test message"
    test_filename = "/Projects/mcap_logger/tests/test_mcap_logger.py"
    test_function = "test_function"
    test_lineno = 69

    with frame_info_mock(
        file_name=test_filename,
        function_name=test_function,
        line_number=test_lineno,
    ):
        # When
        mcap_logger.debug(message)

        # Then
        mocked_logger.debug.assert_called_once_with(message, stacklevel=2)
        expected_log_message = Log(
            timestamp=Timestamp(nanos=0, seconds=int(time.time())),
            level="DEBUG",
            message=message,
            file=f"{test_filename}:{test_function}()",
            line=test_lineno,
        )
        mocked_topic.write.assert_called_once_with(expected_log_message)


@freeze_time("2022-02-03 14:53:23.986")
def test_info_logging(create_mcap_logger):
    # Given
    mcap_logger = create_mcap_logger["mcap_logger"]
    mocked_logger = create_mcap_logger["mocked_logger"]
    mocked_topic = create_mcap_logger["mocked_topic"]
    message = "test message"
    test_filename = "/Projects/mcap_logger/tests/test_mcap_logger.py"
    test_function = "test_function"
    test_lineno = 69

    with frame_info_mock(
        file_name=test_filename,
        function_name=test_function,
        line_number=test_lineno,
    ):
        # When
        mcap_logger.info(message)

        # Then
        mocked_logger.info.assert_called_once_with(message, stacklevel=2)
        expected_log_message = Log(
            timestamp=Timestamp(nanos=0, seconds=int(time.time())),
            level="INFO",
            message=message,
            file=f"{test_filename}:{test_function}()",
            line=test_lineno,
        )
        mocked_topic.write.assert_called_once_with(expected_log_message)


@freeze_time("2022-02-03 14:53:23.986")
def test_warning_logging(create_mcap_logger):
    # Given
    mcap_logger = create_mcap_logger["mcap_logger"]
    mocked_logger = create_mcap_logger["mocked_logger"]
    mocked_topic = create_mcap_logger["mocked_topic"]
    message = "test message"
    test_filename = "/Projects/mcap_logger/tests/test_mcap_logger.py"
    test_function = "test_function"
    test_lineno = 69

    with frame_info_mock(
        file_name=test_filename,
        function_name=test_function,
        line_number=test_lineno,
    ):
        # When
        mcap_logger.warning(message)

        # Then
        mocked_logger.warning.assert_called_once_with(message, stacklevel=2)
        expected_log_message = Log(
            timestamp=Timestamp(nanos=0, seconds=int(time.time())),
            level="WARNING",
            message=message,
            file=f"{test_filename}:{test_function}()",
            line=test_lineno,
        )
        mocked_topic.write.assert_called_once_with(expected_log_message)


@freeze_time("2022-02-03 14:53:23.986")
def test_error_logging(create_mcap_logger):
    # Given
    mcap_logger = create_mcap_logger["mcap_logger"]
    mocked_logger = create_mcap_logger["mocked_logger"]
    mocked_topic = create_mcap_logger["mocked_topic"]
    message = "test message"
    test_filename = "/Projects/mcap_logger/tests/test_mcap_logger.py"
    test_function = "test_function"
    test_lineno = 69

    with frame_info_mock(
        file_name=test_filename,
        function_name=test_function,
        line_number=test_lineno,
    ):
        # When
        mcap_logger.error(message)

        # Then
        mocked_logger.error.assert_called_once_with(message, stacklevel=2)
        expected_log_message = Log(
            timestamp=Timestamp(nanos=0, seconds=int(time.time())),
            level="ERROR",
            message=message,
            file=f"{test_filename}:{test_function}()",
            line=test_lineno,
        )
        mocked_topic.write.assert_called_once_with(expected_log_message)


@freeze_time("2022-02-03 14:53:23.986")
def test_fatal_logging(create_mcap_logger):
    # Given
    mcap_logger = create_mcap_logger["mcap_logger"]
    mocked_logger = create_mcap_logger["mocked_logger"]
    mocked_topic = create_mcap_logger["mocked_topic"]
    message = "test message"
    test_filename = "/Projects/mcap_logger/tests/test_mcap_logger.py"
    test_function = "test_function"
    test_lineno = 69

    with frame_info_mock(
        file_name=test_filename,
        function_name=test_function,
        line_number=test_lineno,
    ):
        # When
        mcap_logger.fatal(message)

        # Then
        mocked_logger.fatal.assert_called_once_with(message, stacklevel=2)
        expected_log_message = Log(
            timestamp=Timestamp(nanos=0, seconds=int(time.time())),
            level="FATAL",
            message=message,
            file=f"{test_filename}:{test_function}()",
            line=test_lineno,
        )
        mocked_topic.write.assert_called_once_with(expected_log_message)


def test_mcap_logger_topic_call(create_mcap_logger):
    # Given
    mcap_logger = create_mcap_logger["mcap_logger"]
    name = "test topic"

    with mock.patch("mcap_logger.mcap_logger.Topic") as mocked_topic_constructor:
        mocked_topic = MagicMock()
        mocked_topic_constructor.return_value = mocked_topic

        # When
        result = mcap_logger.topic(name)

        # Then
        mocked_topic_constructor.assert_called_once_with(
            name, writer=mcap_logger.writer, logger=mcap_logger.logger
        )
        assert result == mocked_topic
