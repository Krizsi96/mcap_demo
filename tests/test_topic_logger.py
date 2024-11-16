from logging import NullHandler
from unittest import mock
from unittest.mock import MagicMock

import pytest
from charset_normalizer.md import getLogger

from mcap_logger.mcap_handler import McapHandler
from mcap_logger.topic_logger import TopicLogger


@pytest.fixture
def create_logger_with_mcap_handler():
    mcap_handler = MagicMock(spec=McapHandler)
    mocked_writer = MagicMock()
    mcap_handler.writer = mocked_writer

    getLogger(__name__).addHandler(mcap_handler)
    yield mocked_writer
    getLogger(__name__).removeHandler(mcap_handler)


def test_topic_logger_initialization_with_existing_mcap_handler(
    create_logger_with_mcap_handler,
):
    # Given
    mocked_writer = create_logger_with_mcap_handler

    # When
    topic_logger = TopicLogger(__name__)

    # Then
    assert topic_logger._writer == mocked_writer


@pytest.fixture
def create_logger_with_null_handler():
    getLogger(__name__).addHandler(NullHandler)
    yield
    getLogger(__name__).removeHandler(NullHandler)


def test_topic_logger_initialization_with_no_mcap_handler(
    create_logger_with_null_handler,
):
    # When
    topic_logger = TopicLogger(__name__)

    # Then
    assert topic_logger._writer is None


def test_topic_logger_topic_call(create_logger_with_mcap_handler):
    # Given
    name = "test_topic"
    topic_logger = TopicLogger(__name__)
    mocked_writer = create_logger_with_mcap_handler

    with mock.patch("mcap_logger.topic_logger.Topic") as mocked_topic_constructor:
        mocked_topic = MagicMock()
        mocked_topic_constructor.return_value = mocked_topic

        # When
        result = topic_logger.topic(name)

        # Then
        mocked_topic_constructor.assert_called_once_with(
            name,
            writer=mocked_writer,
        )
        assert result == mocked_topic
