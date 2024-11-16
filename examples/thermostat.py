import logging
import time
from pathlib import Path

from examples.thermostat_data_pb2 import ThermostatData
from mcap_logger.mcap_handler import McapHandler
from mcap_logger.topic_logger import TopicLogger

THERMOSTAT_DATA = [
    {"temp": 10, "humid": 70},
    {"temp": 5, "humid": 75},
    {"temp": 2, "humid": 78},
    {"temp": -1, "humid": 80},
    {"temp": 3, "humid": 79},
]


def main():  # noqa: ANN201
    logger = logging.getLogger("mcap_logger")
    log_file = Path("thermostat.mcap")
    mcap_handler = McapHandler(log_file)
    mcap_handler.setLevel("DEBUG")

    logger.addHandler(mcap_handler)
    logger.setLevel("DEBUG")

    logger.info("Hello from mcap-logger-tutorial!")

    topic_logger = TopicLogger("mcap_logger")

    for data in THERMOSTAT_DATA:
        time.sleep(0.5)
        temperature = data["temp"]
        humidity = data["humid"]

        thermostat_data = ThermostatData(temperature=temperature, humidity=humidity)
        topic_logger.topic("/thermostat").write(thermostat_data)

        if temperature < 0:
            logger.warning("Temperature is below zero!")


if __name__ == "__main__":
    main()
