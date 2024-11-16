import logging
from pathlib import Path

from foxglove_schemas_protobuf.Log_pb2 import Log
from mcap.reader import make_reader
from mcap_protobuf.decoder import DecoderFactory

from mcap_logger.mcap_handler import McapHandler
from mcap_logger.topic_logger import TopicLogger
from tests.sensor_data_pb2 import SensorData


def test_create_log_with_mcap_handler(tmpdir):
    # Given
    file = Path(str(tmpdir)) / "test.mcap"
    handler = McapHandler(file)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # When
    logger.info("test log")
    # Trigger logfile closing
    logger.removeHandler(handler)
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

            assert proto_msg.level == Log.Level.INFO
            assert proto_msg.message == "test log"


def test_create_data_log_with_topic_logger(tmpdir):
    # Given
    file = Path(str(tmpdir)) / "test.mcap"
    handler = McapHandler(file)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    topic_logger = TopicLogger(__name__)

    temperature = 15
    humidity = 50

    test_message = SensorData(temperature=temperature, humidity=humidity)

    # When
    topic_logger.topic("/test").write(test_message)
    # Trigger logfile closing
    logger.removeHandler(handler)
    handler.close()

    # Then
    assert file.exists()
    with file.open("rb") as f:
        reader = make_reader(f, decoder_factories=[DecoderFactory()])
        messages = list(reader.iter_decoded_messages())

        assert len(messages) == 1

        for schema, channel, message, proto_msg in messages:
            assert schema.name == "SensorData"
            assert schema.encoding == "protobuf"
            assert channel.topic == "/test"

            assert proto_msg.temperature == temperature
            assert proto_msg.humidity == humidity
