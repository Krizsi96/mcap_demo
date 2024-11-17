import logging
import time

from examples.thermostat_data_pb2 import ThermostatData
from mcap_logger.topic_logger import TopicLogger

log = logging.getLogger("library")
log.addHandler(logging.NullHandler())

THERMOSTAT_DATA = [
    {"temp": 10, "humid": 70},
    {"temp": 5, "humid": 75},
    {"temp": 2, "humid": 789},
    {"temp": -1, "humid": 80},
    {"temp": 3, "humid": 79},
]


def get_thermostat_data():  # noqa: ANN201
    for data in THERMOSTAT_DATA:
        humidity = data["humid"]

        if humidity < 0 or humidity > 100:  # noqa: PLR2004
            log.warning("invalid humidity!")
        else:
            yield data


def thermostat_monitor():  # noqa: ANN201
    for data in get_thermostat_data():
        time.sleep(0.5)
        log.debug("got data from thermostat")

        if data["temp"] < 0:
            log.warning("temperature is below zero")

        data_log = ThermostatData(temperature=data["temp"], humidity=data["humid"])
        TopicLogger("library").topic("/thermostat").write(data_log)


if __name__ == "__main__":
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logging.getLogger("library").addHandler(stream_handler)
    logging.getLogger("library").setLevel(logging.DEBUG)

    thermostat_monitor()
