#!/usr/bin/env python3
"""
Example sensor data generator for MIZU Sensor Hub.

This script demonstrates how to send test sensor data to the application
for testing the database functionality.
"""

import time
import random
import json
from datetime import datetime


def generate_sensor_data(device_id="TEST_DEVICE"):
    """Generate realistic sensor data."""
    return {
        "device_id": device_id,
        "ambient_temp": round(random.uniform(20.0, 30.0), 1),
        "humidity": round(random.uniform(40.0, 80.0), 1),
        "soil_moisture": round(random.uniform(30.0, 70.0), 1),
        "soil_temp": round(random.uniform(18.0, 28.0), 1),
        "wind_speed": round(random.uniform(0.0, 15.0), 1),
        "longitude": round(random.uniform(-180.0, 180.0), 4),
        "latitude": round(random.uniform(-90.0, 90.0), 4)
    }


def format_json_data(data):
    """Format data as JSON string."""
    return json.dumps(data)


def format_csv_data(data):
    """Format data as CSV string."""
    return f"{data['device_id']},{data['ambient_temp']},{data['humidity']},{data['soil_moisture']},{data['soil_temp']},{data['wind_speed']},{data['longitude']},{data['latitude']}"


def format_key_value_data(data):
    """Format data as key-value string."""
    return f"device_id={data['device_id']},ambient_temp={data['ambient_temp']},humidity={data['humidity']},soil_moisture={data['soil_moisture']},soil_temp={data['soil_temp']},wind_speed={data['wind_speed']},longitude={data['longitude']},latitude={data['latitude']}"


def main():
    """Main function to generate and display test sensor data."""
    print("MIZU Sensor Hub - Example Sensor Data Generator")
    print("=" * 50)
    print("This script generates example sensor data in various formats.")
    print("You can use this data to test the database functionality.")
    print("=" * 50)

    # Generate sample data
    sensor_data = generate_sensor_data("EXAMPLE_001")

    print(f"\nGenerated sensor data:")
    for key, value in sensor_data.items():
        print(f"  {key}: {value}")

    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Display in different formats
    print("\n" + "=" * 50)
    print("Data in different formats:")

    print("\n1. JSON Format:")
    json_data = format_json_data(sensor_data)
    print(json_data)

    print("\n2. CSV Format:")
    csv_data = format_csv_data(sensor_data)
    print(csv_data)

    print("\n3. Key-Value Format:")
    kv_data = format_key_value_data(sensor_data)
    print(kv_data)

    print("\n" + "=" * 50)
    print("Usage instructions:")
    print("1. Start the MIZU Sensor Hub application")
    print("2. Connect to a serial port (or use a virtual serial port)")
    print("3. Send one of the formatted data strings above")
    print("4. Check the database to see if the data was saved")

    print("\nExample commands to send:")
    print(f"JSON: {json_data}")
    print(f"CSV: {csv_data}")
    print(f"Key-Value: {kv_data}")


if __name__ == "__main__":
    main()
