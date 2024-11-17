from mcap_logger.mcap_logger import get_logger

# Use Console Stream with MCAP Logging

In this tutorial, we will look into how we can combine different log handlers to have console output and MCAP log at the
same time.

## Setup Our Tutorial Project

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

We will change the `hello.py` as shown below.

```python title="hello.py" linenums="1"
import logging
from pathlib import Path

from mcap_logger.mcap_handler import McapHandler


def main():  # noqa: ANN201
    logger = logging.getLogger("mcap_logger")
    log_file = Path("hello.mcap")
    mcap_handler = McapHandler(log_file)
    mcap_handler.setLevel("DEBUG")

    logger.addHandler(mcap_handler)
    logger.setLevel("DEBUG")

    logger.info("Hello from mcap-logger-tutorial!")


if __name__ == "__main__":
    main()

```

## Configure Console Logging

We can see that in our code, we create a logger instance, and we add our `McapHandler` to it as a handler. A Python
logger can have multiple handlers. It can be beneficial for an application to log all messages of all severities to a
file while simultaneously logging warning or above to the console. To set this up, we have to add a `StreamHandler` to
our
logger instance as follows.

```python
stream_handler = logging.StreamHandler()
stream_handler.setLevel("WARNING")

logger.addHandler(stream_handler)
```

Note, that we can set the logging level separately from other handlers and from the logger. In this case, becasue the
level of the `logger` is `DEBUG`, it will forward all log messages to the handlers. The `mcap_handler` has also `DEBUG`
level, so it will log every messages to the log file. The `stream_handler` has `WARNING` log level, which means that it
will only print messages that are `WARNING` or prior to `WARNING`.

!!! tip "Logging Flow"

    [Here](https://docs.python.org/3/howto/logging.html#logging-flow) you can check the flowdiagram of the logging.

We can add a `warning` message to our `hello.py` script to see the behaviour described above. After the modifications
our `hello.py` script should look like this.

```python title="hello.py" linenums="1"
import logging
from pathlib import Path

from mcap_logger.mcap_handler import McapHandler


def main():  # noqa: ANN201
    logger = logging.getLogger("mcap_logger")
    log_file = Path("hello.mcap")
    mcap_handler = McapHandler(log_file)
    mcap_handler.setLevel("DEBUG")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel("WARNING")

    logger.addHandler(mcap_handler)
    logger.addHandler(stream_handler)
    logger.setLevel("DEBUG")

    logger.info("Hello from mcap-logger-tutorial!")
    logger.warning("This is a warning")


if __name__ == "__main__":
    main()

```

## Running The Script

```shell
uv run hello.py
```

When we run the command above, we should see that the warning message is printed on our console (and the info message is
not), and also that we have a `hello.mcap` file in our folder that contains both the warning message and the info
message.

## Code Structuring

Our code is functional, however it is really verbose and suppress the essential parts of the `main` function (the two
log messages 😄). We can move the technical details of the logger to its own function, so that all the logger
configuration can live in one place. We should also move the `logger` variable out to the global scope so that any
function in the script can access it.

```python title="hello.py" linenums="1"
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


log_file = Path("hello.mcap")
log = get_logger("mcap_logger", log_file)


def main():  # noqa: ANN201
    log.info("Hello from mcap-logger-tutorial!")
    log.warning("This is a warning")


if __name__ == "__main__":
    main()

```

With this, we have a simple example that how we can configure a logger with both console and MCAP logging.

!!! tip "Configuring Logging"

    To learn about more advanced logging configuration, please check out the
    [Logging HOWTO - Configuring Logging](https://docs.python.org/3/howto/logging.html#configuring-logging) section
