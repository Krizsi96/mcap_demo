# MCAP Logger 🧢

This python package wraps the [MCap protobuf logging package](https://mcap.dev/docs/python/protobuf_example) with
the [Foxglove schemas](https://docs.foxglove.dev/docs/visualization/message-schemas/introduction/) to provide a
standardised, easy to import and use logging method.

## Usage

1. Add the package to your python project.
2. Import the package and use the `get_logger` function to create your logger.

```python
from mcap_logger.mcap_logger import get_logger

logger = get_logger(__name__)
```

3. If you haven't provided any log file path and or log level to the `get_logger` function, you can use environmental
   variables to specify them at run time. `LOG_LEVEL` for log level, and `LOG_ROOT` for the log file.

```shell
LOG_LEVEL=DEBUG LOG_ROOT=log_file.mcap uv run python -m mcap.demo.demo
```

4. Use the MCAPLogger `.debug()`, `.info()`, `.warning()`, etc. functions to create different types of log messages
5. If you want to log topics like sensor data, you have to first specify the message with protobuf. (See
   the [Working with ProtoBuf](#working-with-protobuf) section).
6. You can open the created log file with [Foxglove Studio](https://foxglove.dev/).

For an example see [demo.py](mcap_logger/demo/demo.py).

The output: ![demo_log_in_foxglove.png](docs/demo_log_in_foxglove.png)

## Working with ProtoBuf

Protocol buffers are Google's language-neutral mechanism for serializing structured data.
>ℹ️ More info about it and its
syntax: [Protocol Buffers](https://protobuf.dev/)

1. Make sure that you have the latest protobuf-compiler installed
   [protoc installation](https://grpc.io/docs/protoc-installation/)
2. You can compile the `.proto` file with the following command.

Example:

```bash
protoc --python_out=. sensor_data.proto
```

3. Import the created protobuf python script (this can confuse your linter).
4. Create a protobuf message and use the `.topic().write()` function to log the message.

Example:

```python
from mcap_logger.demo.sensor_data_pb2 import SensorData

sensor_message = SensorData(temperature=25, humidity=65)
logger.topic("/sensor_data").write(sensor_message)
```
