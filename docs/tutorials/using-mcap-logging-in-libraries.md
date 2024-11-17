from logging import NullHandlerfrom examples.library import thermostat_monitor

# Using MCAP Logging in Libraries

This tutorial will show you how the logging should be handled in libraries.

## Setup our tutorial project

!!! note ""

    In this tutorial we will use `uv`.

Let's [create a new uv project](https://docs.astral.sh/uv/guides/projects/) and
[add the MCAP Logger](installation.md) package as dependency.

```shell
uv init mcap_logger_tutorial
cd mcap_logger_tutorial
uv add mcap-logger
```

After this we should have the following elements in the project's folder:

```
.
├── .python-version
├── README.md
├── hello.py
└── pyproject.toml
```

We will replace the `hello.py` script with `application.py` adn `library.py`.

```python title="application.py" linenums="1"
import logging
from pathlib import Path

from mcap_logger.mcap_handler import McapHandler


def get_logger(name: str, file: Path) -> logging.Logger:
    logger = logging.getLogger(name)
    mcap_handler = McapHandler(file)
    mcap_handler.setLevel("DEBUG")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel("WARNING")

    logger.addHandler(mcap_handler)
    logger.addHandler(stream_handler)
    logger.setLevel("DEBUG")
    return logger


log_file = Path("application.mcap")
log = get_logger("mcap_logger", log_file)


def main():  # noqa: ANN201
    log.info("Hello from mcap-logger-tutorial!")


if __name__ == "__main__":
    main()

```

The `application.py` is just our `examples/hello.py` example, and it only logs a log message.

```python title="library.py" linenums="1"
THERMOSTAT_DATA = [
    {"temp": 10, "humid": 70},
    {"temp": 5, "humid": 75},
    {"temp": 2, "humid": 78},
    {"temp": -1, "humid": 110},
    {"temp": 3, "humid": 79},
]


def get_thermostat_data():
    for data in THERMOSTAT_DATA:
        humidity = data["humid"]

        if humidity < 0 or humidity > 100:
            print("invalid humidity!")
        else:
            yield data


if __name__ == "__main__":
    for data in get_thermostat_data():
        print(data)

```

The `library.py` is a modification of our `examples/thermostat.py` script. In this version we have the
`get_thermostat_data` function, that yields back the data from the `THERMOSTAT_DATA` array, when the data is valid. If
the humidity is out of boundaries then it will print a message to the console.

We can run this library example with `uv run library.py` and see the printed out data and the error message.

```shell
{'temp': 10, 'humid': 70}
{'temp': 5, 'humid': 75}
{'temp': 2, 'humid': 78}
invalid humidity!
{'temp': 3, 'humid': 79}
```

## Import our library into our application

Now, we will import this simple library into our application, and call its `get_thermostat_data` function in a for-loop.
We will also simulate the time passing with a `time.sleep` call. After the `log.info` call we should add the following
code.

```python title="application.py"
for data in get_thermostat_data():
    time.sleep(0.5)
    log.debug("fetching data from thermostat")
```

When we run this code that we can see the warning message on the console and that the `.mcap` log file was created with
all the log messages we created except the library's logs.

However, using `print` statements should be avoided, so we have to create a logger for our library.

## Creating logger for our library

!!! info

    Python's Logging HOWTO guide has a nice documentation on how to
    [configure logging for a library](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library)

The application developer knows their target audience and what handlers are most appropriate for their application. So
we have to give the application full control over how the library does the logging. Our library should create a logger
with a unique and easily identifiable name, and we should not add any handlers to it other than `NullHandler`.

A [NullHandler](https://docs.python.org/3/library/logging.handlers.html#logging.NullHandler) is a 'do nothing' handler,
and we can use it to assure that our logger won't fall back to the `LastResort` handler.

Loggers are hierarchical, and they inherit configurations from the top-level logger. If all logging by a library `foo`
is done using loggers with names matching `foo.x`, `foo.y`, etc. then we can configure the `NullHandler` only for the
top-level logger of the library like the following code.

```python
import logging

logging.getLogger('foo').addHandler(logging.NullHandler())
```

In our case, we have only one library script, so we will configure our logger in it. In the `library.py` we import the
`logging` package and create our logger instance called by `library`. Then we add the `NullHandler` to the library's
logger.

!!! tip

    Use a logger with a unique and easily identifiable name, such as the `__name__` for your library’s top-level package
    or module.

```python title="library.py"
import logging

log = logging.getLogger("library")
log.addHandler(logging.NullHandler())
```

Then we should replace the `print` statements with logger calls.

```python title="library.py"
log.warning("invalid humidity!")
```

and

```python title="library.py"
log.info(data)
```

If we run now our library standalone, we can see that no output is generated on the console. This is because all the
logs are handed over to the `NullHandler` which discards them.

We can change this behavior for the standalone run if we change the configuration of the logger when we only run the
library script. The code belows shows how our library script should look like after the changes.

```python title="library.py"
import logging

log = logging.getLogger("library")
log.addHandler(logging.NullHandler())

THERMOSTAT_DATA = [
    {"temp": 10, "humid": 70},
    {"temp": 5, "humid": 75},
    {"temp": 2, "humid": 78},
    {"temp": -1, "humid": 110},
    {"temp": 3, "humid": 79},
]


def get_thermostat_data():
    for data in THERMOSTAT_DATA:
        humidity = data["humid"]

        if humidity < 0 or humidity > 100:
            log.warning("invalid humidity!")
        else:
            yield data


if __name__ == "__main__":
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logging.getLogger("library").addHandler(stream_handler)
    logging.getLogger("library").setLevel(logging.DEBUG)

    for data in get_thermostat_data():
        log.info(data)

```

!!! note

    Loggers are [singletons](https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/),
    this means the only one instance of a logger with a given name exists. When you call the `getLogger` function with
    an existing name, then it will return that singleton.

## Configure the library logger from application

Now, that we have library with logging, we have to configure its logger from our application if we want to use it.
We have many possibilities on how we could configure the logger, for now, let's say that we want the library to use the
same level of logging as the application logger, and it should also log to the same file.

We will add this configuration step into our `get_logger` function, where we defined the `StreamHandler` and
`McapHandler` for our application logging. We just have to add the same handler to the library's logger as follows.

```python title="application.py"
def get_logger(name: str, file: Path) -> logging.Logger:
    logger = logging.getLogger(name)
    mcap_handler = McapHandler(file)
    mcap_handler.setLevel("DEBUG")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel("DEBUG")

    logger.addHandler(mcap_handler)
    logger.addHandler(stream_handler)
    logger.setLevel("DEBUG")

    library_logger = logging.getLogger("library")
    library_logger.addHandler(stream_handler)
    library_logger.addHandler(mcap_handler)

    return logger

```

When we run the application now, we should see all the log messages on the console and in the `.mcap` file.

```shell title="applciation.mcap"
[ INFO][12:40:34.683 PM CET][application]: Hello from mcap-logger-tutorial!
[DEBUG][12:40:35.184 PM CET][application]: fetching data from thermostat
[DEBUG][12:40:35.684 PM CET][application]: fetching data from thermostat
[DEBUG][12:40:36.184 PM CET][application]: fetching data from thermostat
[ WARN][12:40:36.184 PM CET][library]: invalid humidity!
[DEBUG][12:40:36.684 PM CET][application]: fetching data from thermostat
```

As you can see, this approach gives us plenty of opportunity to fine tune the logging behaviour of our library from our
application. We configure the library logger to only log higher severity message on the console and the mcap file. Or
log into a different mcap file or not to do file logging at all. The choice is in the application developer to figure
out what makes sense for them.

!!! warning "Take care to document how your library uses logging - for example, the names of loggers used."

## Adding data logging

Following the rule of thumb for how to configure library logging, we can see that we should not let our library populate
our system with data log files whenever we run it. As before this should be up to the application developer.

To achieve this we should follow the following rules:

1. Functions that don't run as a process, must not create `topic` logs.
2. Functions that run as a process, should create `topic` logs.
3. ProtoBuf file should be provided for `topic` logs.

Let's see two scenarios to see the difference.

### Data logging from application

Given that we have the following `aplication.py` script.

```python title="application.py" linenums="1"
import logging
import time
from pathlib import Path

from examples.library import get_thermostat_data
from mcap_logger.mcap_handler import McapHandler


def get_logger(name: str, file: Path) -> logging.Logger:
    logger = logging.getLogger(name)
    mcap_handler = McapHandler(file)
    mcap_handler.setLevel("DEBUG")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel("DEBUG")

    logger.addHandler(mcap_handler)
    logger.addHandler(stream_handler)
    logger.setLevel("DEBUG")

    library_logger = logging.getLogger("library")
    library_logger.addHandler(stream_handler)
    library_logger.addHandler(mcap_handler)

    return logger


log_file = Path("application.mcap")
log = get_logger("mcap_logger", log_file)


def main():
    log.info("Hello from mcap-logger-tutorial!")

    for data in get_thermostat_data():
        time.sleep(0.5)
        log.debug("fetching data from thermostat")


if __name__ == "__main__":
    main()

```

Let's say that we want to log the thermostat data from our application to the mcap file. In this case, we should import
the PotoBuf script of the thermostat data into our `applicaton.py` script and call the `TopicLogger` from there.

```python title="application.py" linenums="1"
import logging
import time
from pathlib import Path

from examples.library import get_thermostat_data
from examples.thermostat_data_pb2 import ThermostatData
from mcap_logger.mcap_handler import McapHandler
from mcap_logger.topic_logger import TopicLogger


def get_logger(name: str, file: Path) -> logging.Logger:
    logger = logging.getLogger(name)
    mcap_handler = McapHandler(file)
    mcap_handler.setLevel("DEBUG")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel("DEBUG")

    logger.addHandler(mcap_handler)
    logger.addHandler(stream_handler)
    logger.setLevel("DEBUG")

    library_logger = logging.getLogger("library")
    library_logger.addHandler(stream_handler)
    library_logger.addHandler(mcap_handler)

    return logger


log_file = Path("application.mcap")
log = get_logger("mcap_logger", log_file)


def main():
    log.info("Hello from mcap-logger-tutorial!")

    for data in get_thermostat_data():
        time.sleep(0.5)
        log.debug("fetching data from thermostat")
        data_log = ThermostatData(temperature=data["temp"], humidity=data["humid"])
        TopicLogger("mcap_logger").topic("/thermostat").write(data_log)


if __name__ == "__main__":
    main()

```

In this scenario, the library is only used to get the data from our "sensor", and because of this it is the applications
choice and responsibility to log it.

### Data logging from library

It is possible that the library has functions that can be imported and run as a process by other scripts. For example,
lets add a `thermostat_monitor` to our library, that fetches the data from the thermostat, logs the data and creates a
warning log if the temperature is below zero.

```python title="library.py" linenums="1"
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


def get_thermostat_data():
    for data in THERMOSTAT_DATA:
        humidity = data["humid"]

        if humidity < 0 or humidity > 100:
            log.warning("invalid humidity!")
        else:
            yield data


def thermostat_monitor():
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

```

The monitor function can be imported by another script and run it as a process until all the data is
fetched. In this case, the monitor function does the logging, but only if the given logger name has an `McapHandler`
added to it. If no, then the topic log will be discarded.

From the application side, we will configure the logger of the library and run the `thermostat_monitor` function.

```python title="application.py" linenums="1"
import logging
from pathlib import Path

from examples.library import thermostat_monitor
from mcap_logger.mcap_handler import McapHandler


def get_logger(name: str, file: Path) -> logging.Logger:
    logger = logging.getLogger(name)
    mcap_handler = McapHandler(file)
    mcap_handler.setLevel("DEBUG")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel("INFO")

    logger.addHandler(mcap_handler)
    logger.addHandler(stream_handler)
    logger.setLevel("DEBUG")

    library_logger = logging.getLogger("library")
    library_logger.setLevel("DEBUG")
    library_logger.addHandler(stream_handler)
    library_logger.addHandler(mcap_handler)

    return logger


log_file = Path("application.mcap")
log = get_logger("mcap_logger", log_file)


def main():
    log.info("Hello from mcap-logger-tutorial!")
    thermostat_monitor()


if __name__ == "__main__":
    main()

```

When we run the application, then we should see the info and warning messages, and in the `.mcap` file we should see all
the log messages.
