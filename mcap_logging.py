import inspect
import time

from foxglove_schemas_protobuf.Log_pb2 import Log
from mcap_protobuf.writer import Writer
from google.protobuf.timestamp_pb2 import Timestamp
from sensor_data_pb2 import SensorData

TEMPERATURE_DATA = [10, 5, 2, -1, 3]
HUMIDITY_DATA = [70, 75, 78, 80, 79]

SENSOR_DATA = [
    {"temp": 10, "humid": 70},
    {"temp": 5, "humid": 75},
    {"temp": 2, "humid": 78},
    {"temp": -1, "humid": 80},
    {"temp": 3, "humid": 79},
]

def main():
    with open("test_log.mcap", "wb") as f, Writer(f) as mcap_writer:
        for i, sensor_data in enumerate(SENSOR_DATA):
            timestamp = i * 1_000_000_000
            temperature = sensor_data.get("temp")
            humidity = sensor_data.get("humid")

            sensor_message = SensorData(
                temperature=temperature,
                humidity=humidity
            )
            print(f"{sensor_message=}")

            mcap_writer.write_message(
                topic="/sensor_data",
                message=sensor_message,
                log_time=timestamp,
                publish_time=timestamp,
            )

            if temperature < 0:
                log_message = log_warning("Temperature is below 0!")
                print(f"{log_message=}")

                mcap_writer.write_message(
                    topic="/log_messages",
                    message=log_message,
                    log_time=timestamp,
                    publish_time=timestamp,
                )
    print("logging finished")

def log_warning(message: str) -> Log:
    previous_frame = inspect.currentframe().f_back
    (
        filename,
        line_number,
        function_name,
        lines,
        index,
    ) = inspect.getframeinfo(previous_frame)

    return Log (
        timestamp=Timestamp(nanos=0, seconds=int(time.time())),
        level="WARNING",
        message=message,
        file=f'{filename}:{function_name}()',
        line=line_number,
    )


if __name__ == "__main__":
    main()