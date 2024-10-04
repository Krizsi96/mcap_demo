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
        sensor_data_topic = Topic(name="/sensor_data", writer=mcap_writer)
        log = MCAPLog(mcap_writer)
        for i, sensor_data in enumerate(SENSOR_DATA):
            temperature = sensor_data.get("temp")
            humidity = sensor_data.get("humid")

            sensor_message = SensorData(
                temperature=temperature,
                humidity=humidity
            )
            print(f"{sensor_message=}")

            sensor_data_topic.send(sensor_message)

            if temperature < 0:
                log.warning("Temperature is below 0!")

    print("logging finished")

class MCAPLog:
    def __init__(self, writer: Writer) -> None:
        self.writer = writer
        self.log_topic = Topic(name="/log", writer=writer)

    def warning(self, message: str) -> None:
        previous_frame = inspect.currentframe().f_back
        (
            filename,
            line_number,
            function_name,
            lines,
            index,
        ) = inspect.getframeinfo(previous_frame)

        log_message = Log(
            timestamp=Timestamp(nanos=0, seconds=int(time.time())),
            level="WARNING",
            message=message,
            file=f'{filename}:{function_name}()',
            line=line_number,
        )
        print(log_message)

        self.log_topic.send(log_message)



class Topic:
    def __init__(self, name: str, writer: Writer) -> None:
        self.name = name
        self.writer = writer

    def send(self, message: Log) -> None:
        timestamp = int(time.time())
        self.writer.write_message(
            topic=self.name,
            message=message,
            log_time=timestamp,
            publish_time=timestamp,
        )


if __name__ == "__main__":
    main()