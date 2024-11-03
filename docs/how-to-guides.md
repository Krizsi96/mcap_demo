## How To Set The Log File And Log Level For Multiple Scripts

Given that you have a Python project that contains multiple modules that are using the `mcap-logger`. The problem you
have is that in order to set the `log file` and `log level`, you have to change the code in each module.

To avoid this issue, `mcap-logger` can work with environmental variables to set these parameters. `LOG_LEVEL` for log
level, and `LOG_ROOT` for the log file.

1. Import the package into your module and use the `get_logger` function to create your logger as follows.

```python
from mcap_logger.mcap_logger import get_logger

logger = get_logger(__name__)
```

2. Run your script with the environmental variables defined in your command. Example:

```shell
LOG_LEVEL=DEBUG LOG_ROOT=log_file.mcap uv run python -m mcap.demo.demo
```
