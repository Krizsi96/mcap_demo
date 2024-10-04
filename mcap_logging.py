
from foxglove_schemas_protobuf.Log_pb2 import Log
from mcap_protobuf.writer import Writer
from google.protobuf.timestamp_pb2 import Timestamp
from foxglove_schemas_protobuf.KeyValuePair_pb2 import KeyValuePair

TEMPERATURE_DATA = [10, 5, 2, -1, 3]
HUMIDITY_DATA = [70, 75, 78, 80, 79]

def main():
    with open("test_log.mcap", "wb") as f, Writer(f) as mcap_writer:
        for i, temperature in enumerate(TEMPERATURE_DATA):
            temperature_message = KeyValuePair(key="temperature", value=f'{temperature}')

            mcap_writer.write_message(
                topic="/sensor_data",
                message=temperature_message,
                log_time=i * 1000,
                publish_time=i * 1000,
            )

            log_message = Log (
                timestamp=Timestamp().GetCurrentTime(),
                level="WARNING",
                message=f"this is a log {i}",
                file="random.py",
                line=69,
            )
            print(f"{log_message=}")

            mcap_writer.write_message(
                topic="/log_messages",
                message=log_message,
                log_time=i * 1000,
                publish_time=i * 1000,
            )
    print("logging finished")


if __name__ == "__main__":
    main()