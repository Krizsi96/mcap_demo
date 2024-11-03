# MCAP Logger 🧢

## Project description

This python package to provide a standardised, easy to import and use logging method.

The package is...

- a logger module that leverages the existing MCAP and Foxglove packages
- provides a plugin replacement for standard Python login
- provides console logging with configurable log level and handled separately from the file's

Links:

- [Documentation](https://8-bit-hunters.github.io/mcap_logger/)
- [PyPI package](https://pypi.org/project/mcap-logger/)

## Example usage

### Installing the library

```shell
pip install mcap-logger
```

### Creating a simple log

```python
# Import the library
from mcap_logger.mcap_logger import get_logger

# Get MCAP logger instance
logger = get_logger(__name__)

logger.info("Hello, World!")

```

### Log Protobuf data

> ℹ️ Protocol buffers are Google's language-neutral mechanism for serializing structured data. More info about it and
> its syntax: [Protocol Buffers](https://protobuf.dev/)

```python
# Import the library
from mcap_logger.mcap_logger import get_logger

# Import Protobuf class
from mcap_logger.demo.sensor_data_pb2 import SensorData

# Get MCAP logger instance
logger = get_logger(__name__)

# Log Protobuf data
sensor_message = SensorData(temperature=25, humidity=65)
logger.topic("/sensor_data").write(sensor_message)

```

![](docs/assets/demo_log_in_foxglove.png)

## Call for Contributions

The MCAP-Logger project welcomes your expertise and enthusiasm!
