from mcap.writer import Writer
from time import time_ns
import time
# Sample sensor readings
sensor_readings = [10, 8, 3, -1, 4, 5]

# Define the file path where the MCAP file will be stored
file_path = "temperature_sensor.mcap"

# Open a file to write the MCAP data
with open(file_path, "wb") as f:
    writer = Writer(f)

    # Start a new MCAP recording
    writer.start()

    # Register a schema (optional, since we'll be writing simple JSON messages)
    schema_id = writer.register_schema(
        name="temperature-schema",
        encoding="jsonschema",
        data=b''  # JSON encoding
    )

    # Register a channel for the temperature sensor data
    temp_channel_id = writer.register_channel(
        topic="temperature_sensor",
        message_encoding="json",
        schema_id=schema_id
    )

    # Register a channel specifically for logging messages
    log_channel_id = writer.register_channel(
        topic="application_logs",
        message_encoding="json",
        schema_id=schema_id
    )

    # Loop through the sensor readings and log them to the MCAP file
    for reading in sensor_readings:
        # Get the current timestamp in nanoseconds
        timestamp_ns = time_ns()

        # Create the JSON data to log the temperature reading
        message_data = f'{{"temperature": {reading}}}'.encode()

        # Write the temperature reading to the MCAP file
        writer.add_message(
            channel_id=temp_channel_id,
            log_time=timestamp_ns,
            publish_time=timestamp_ns,
            data=message_data
        )

        # Check if the temperature goes below 0, and log an error if so
        if reading < 0:
            warning_message = f'{{"level": "WARNING", "message": "Temperature below zero: {reading}C"}}'.encode()

            # Write the error message to the MCAP file
            writer.add_message(
                channel_id=log_channel_id,
                log_time=timestamp_ns,
                publish_time=timestamp_ns,
                data=warning_message
            )

        # Sleep for 1 second to simulate collecting data every second
        time.sleep(1)

    # Finalize the MCAP recording
    writer.finish()

print("Sensor data and errors logged to MCAP file.")