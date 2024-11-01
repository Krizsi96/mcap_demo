import time
from unittest import mock

from freezegun import freeze_time

from mcap_logger.mcap_logger import Topic


@mock.patch("mcap_logger.mcap_logger.logging.Logger")
@mock.patch("mcap_logger.mcap_logger.Writer")
def test_topic_initialisation_with_console_logger(mock_writer, mock_logger):
    # Given
    name = "test name"

    # When
    topic = Topic(name, mock_writer, mock_logger)

    # Then
    assert topic.name == name
    assert topic.writer == mock_writer
    assert topic.logger == mock_logger


@mock.patch("mcap_logger.mcap_logger.Writer")
def test_topic_initialisation_without_console_logger(mock_writer):
    # Given
    name = "test name"

    # When
    topic = Topic(name, mock_writer)

    # Then
    assert topic.name == name
    assert topic.writer == mock_writer
    assert topic.logger is None


@freeze_time("2022-02-03 14:53:00")
@mock.patch("mcap_logger.mcap_logger.logging.Logger")
@mock.patch("mcap_logger.mcap_logger.Writer")
def test_writing_message_to_topic_with_console_logger(
    mocked_writer, mocked_console_logger
):
    # Given
    topic = Topic("test topic", mocked_writer, mocked_console_logger)
    message = "test message"

    # When
    topic.write(message)

    # Then
    mocked_console_logger.debug.assert_called_once_with(
        f"{topic.name} topic:\n{message=}"
    )
    mocked_writer.write_message.assert_called_once_with(
        topic=topic.name,
        message=message,
        log_time=time.time_ns(),
        publish_time=time.time_ns(),
    )


@freeze_time("2022-02-03 14:53:00")
@mock.patch("mcap_logger.mcap_logger.Writer")
def test_writing_message_to_topic_without_console_logger(mocked_writer):
    # Given
    topic = Topic("test topic", mocked_writer)
    message = "test message"

    # When
    topic.write(message)

    # Then
    mocked_writer.write_message.assert_called_once_with(
        topic=topic.name,
        message=message,
        log_time=time.time_ns(),
        publish_time=time.time_ns(),
    )
