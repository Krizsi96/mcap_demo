import time
from unittest import mock

from freezegun import freeze_time

from mcap_logger.topic_logger import Topic


@mock.patch("mcap_logger.topic_logger.Writer")
def test_topic_initialisation_with_console_logger(mock_writer):
    # Given
    name = "test name"

    # When
    topic = Topic(name, mock_writer)

    # Then
    assert topic._name == name
    assert topic._writer == mock_writer


@freeze_time("2022-02-03 14:53:00")
@mock.patch("mcap_logger.topic_logger.Writer")
def test_writing_message_to_topic(mocked_writer):
    # Given
    topic = Topic("test topic", mocked_writer)
    message = "test message"

    # When
    topic.write(message)

    # Then
    mocked_writer.write_message.assert_called_once_with(
        topic=topic._name,
        message=message,
        log_time=time.time_ns(),
        publish_time=time.time_ns(),
    )


def test_writing_message_to_topic_without_write():
    # Given
    writer = None
    topic = Topic("test topic", writer)
    message = "test message"

    # When
    topic.write(message)

    # Then
    # No error
