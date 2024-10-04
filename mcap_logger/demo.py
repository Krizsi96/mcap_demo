import inspect
import time
from inspect import Traceback
from pathlib import Path
from typing import Any

from foxglove_schemas_protobuf.Log_pb2 import Log
from mcap_protobuf.writer import Writer
from google.protobuf.timestamp_pb2 import Timestamp
from sensor_data_pb2 import SensorData

SENSOR_DATA = [
    {"temp": 10, "humid": 70},
    {"temp": 5, "humid": 75},
    {"temp": 2, "humid": 78},
    {"temp": -1, "humid": 80},
    {"temp": 3, "humid": 79},
]

def main():
    logger = MCAPLogger(Path("test_log.mcap"))
    for i, sensor_data in enumerate(SENSOR_DATA):
        time.sleep(1)
        temperature = sensor_data["temp"]
        humidity = sensor_data["humid"]

        sensor_message = SensorData(
            temperature=temperature,
            humidity=humidity
        )
        logger.topic("/sensor_data").write(sensor_message)

        if temperature < 0:
            logger.warning("Temperature is below zero!")

    print("logging finished")



class Topic:
    def __init__(self, name: str, writer: Writer) -> None:
        self.name = name
        self.writer = writer

    def write(self, message: Any) -> None:
        timestamp = int(time.time()) * 1_000_000_000
        print(f"saving message:\n{message}")
        self.writer.write_message(
            topic=self.name,
            message=message,
            log_time=timestamp,
            publish_time=timestamp,
        )

class MCAPLogger:
    def __init__(self, log_file: Path) -> None:
        print(f"Creating logger for {log_file}")
        self.log_file = open(str(log_file), "wb")
        self.writer = Writer(self.log_file)
        self.log_topic = Topic(name="/log", writer=self.writer)

    def __del__(self):
        self.writer.finish()

    def warning(self, message: str) -> None:
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self._write_log(level="WARNING", message=message, traceback=traceback)


    def _write_log(self, level: str, message: str, traceback: Traceback) -> None:
        traceback.
        log_message = Log(
            timestamp=Timestamp(nanos=0, seconds=int(time.time())),
            level=level,
            message=message,
            file=f'{traceback.filename}:{traceback.function}()',
            line=traceback.lineno,
        )
        self.log_topic.write(log_message)


    def topic(self, name: str) -> Topic:
        return Topic(name, writer=self.writer)

if __name__ == "__main__":
    main()