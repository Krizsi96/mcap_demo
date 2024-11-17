In the past we were relying on console printouts and unserialised log files to log the actions of our systems. As the
complexity of the system increased, so did the amount and complexity of the logged data, and the previous approach was
not feasible anymore.

Fortunately, there is already solutions like [MCAP](mcap.md) and [Foxglove](foxglove.md), that combined
with [ProtoBuf](protobuf.md) allows us to make smaller sized logs with better traceability.

Python packages like [mcap-protobuf-support](https://pypi.org/project/mcap-protobuf-support/)
and [foxglove-schemas-protobuf](https://pypi.org/project/foxglove-schemas-protobuf/) are nice implementations to achieve
this.

The goal of this package is...

- to create a logger handler that leverages the existing MCAP and Foxglove packages
- to leverage the configurability of Python
- to provide a plugin for standard Python loging
