In the past we were relying on console printouts and unserialised log files to log the actions of our systems. As the
complexity of the system increased, so did the amount and complexity of the logged data, and the previous approach was
not feasible anymore.

Fortunately, there is already solutions like [MCAP](mcap.md) and [Foxglove](foxglove.md), that combined
with [ProtoBuf](protobuf.md) allows us to make smaller sized logs with better traceability.

Python packages like [mcap-protobuf-support](https://pypi.org/project/mcap-protobuf-support/)
and [foxglove-schemas-protobuf](https://pypi.org/project/foxglove-schemas-protobuf/) are nice implementations to achieve
this.

The goal of this package is...

- to create a logger module that leverages the existing MCAP and Foxglove packages
- to provide a plugin replacement for standard Python login
- to provide console logging with configurable log level and handled separately from the file's
