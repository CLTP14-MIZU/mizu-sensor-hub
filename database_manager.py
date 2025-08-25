"""
Database manager for MIZU Sensor Hub.

This module handles all database operations including saving sensor data
and managing database connections.
"""

import re
from typing import Optional, Dict, Any
from database_models import SensorData, get_db_session, init_database


class DatabaseManager:
    """
    Manages database operations for sensor data storage.

    This class handles saving sensor data to the PostgreSQL database
    and provides methods for data retrieval and management.
    """

    def __init__(self, database_url: str):
        """
        Initialize the database manager.

        Args:
            database_url: SQLAlchemy database URL
        """
        self.database_url = database_url
        self._initialized = False

    def initialize(self) -> bool:
        """
        Initialize the database connection and create tables.

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            init_database(self.database_url)
            self._initialized = True
            print(f"Database initialized successfully: {self.database_url}")
            return True
        except Exception as e:
            print(f"Failed to initialize database: {e}")
            return False

    def save_sensor_data(self, data_string: str) -> bool:
        """
        Parse sensor data from string and save to database.

        Args:
            data_string: Raw sensor data string from serial connection

        Returns:
            True if data saved successfully, False otherwise
        """
        if not self._initialized:
            print("Database not initialized. Cannot save data.")
            return False

        try:
            # Parse the sensor data
            sensor_data = self._parse_sensor_data(data_string)
            if not sensor_data:
                return False

            # Save to database
            db = get_db_session()
            try:
                new_record = SensorData(**sensor_data)
                db.add(new_record)
                db.commit()
                print(f"Saved sensor data to database: {sensor_data}")
                return True
            except Exception as e:
                db.rollback()
                print(f"Failed to save sensor data: {e}")
                return False
            finally:
                db.close()

        except Exception as e:
            print(f"Error processing sensor data: {e}")
            return False

    def _parse_sensor_data(self, data_string: str) -> Optional[Dict[str, Any]]:
        """
        Parse sensor data from the received string.

        This method attempts to extract sensor values from various
        common data formats. You may need to adjust the parsing logic
        based on your specific sensor data format.

        Args:
            data_string: Raw sensor data string

        Returns:
            Dictionary with parsed sensor data or None if parsing fails
        """
        # Remove whitespace and newlines
        data_string = data_string.strip()

        # Try to parse JSON-like format
        if data_string.startswith('{') and data_string.endswith('}'):
            return self._parse_json_format(data_string)

        # Try to parse key-value format (check before CSV since key-value also contains commas)
        if '=' in data_string:
            return self._parse_key_value_format(data_string)

        # Try to parse CSV-like format
        if ',' in data_string:
            return self._parse_csv_format(data_string)

        # If no specific format detected, try to extract numbers
        return self._parse_generic_format(data_string)

    def _parse_json_format(self, data_string: str) -> Optional[Dict[str, Any]]:
        """Parse JSON-like format data."""
        try:
            import json
            data = json.loads(data_string)

            return {
                'device_id': str(data.get('device_id', 'unknown')),
                'ambient_temperature': self._safe_float(data.get('ambient_temp')),
                'humidity': self._safe_float(data.get('humidity')),
                'soil_moisture': self._safe_float(data.get('soil_moisture')),
                'soil_temperature': self._safe_float(data.get('soil_temp')),
                'wind_speed': self._safe_float(data.get('wind_speed')),
                'longitude': self._safe_float(data.get('longitude')),
                'latitude': self._safe_float(data.get('latitude')),
                'transmitted': False
            }
        except Exception:
            return None

    def _parse_csv_format(self, data_string: str) -> Optional[Dict[str, Any]]:
        """Parse CSV-like format data."""
        try:
            parts = data_string.split(',')
            if len(parts) >= 5:
                return {
                    'device_id': str(parts[0].strip()),
                    'ambient_temperature': self._safe_float(parts[1]),
                    'humidity': self._safe_float(parts[2]),
                    'soil_moisture': self._safe_float(parts[3]),
                    'soil_temperature': self._safe_float(parts[4]),
                    'wind_speed': self._safe_float(parts[5]) if len(parts) > 5 else None,
                    'longitude': self._safe_float(parts[6]) if len(parts) > 6 else None,
                    'latitude': self._safe_float(parts[7]) if len(parts) > 7 else None,
                    'transmitted': False
                }
        except Exception:
            pass
        return None

    def _parse_key_value_format(self, data_string: str) -> Optional[Dict[str, Any]]:
        """Parse key=value format data."""
        try:
            data = {}
            pairs = data_string.split(',')

            for pair in pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    key = key.strip().lower()
                    value = value.strip()

                    if key == 'device_id':
                        data['device_id'] = value
                    elif key == 'ambient_temp':
                        data['ambient_temperature'] = self._safe_float(value)
                    elif key == 'humidity':
                        data['humidity'] = self._safe_float(value)
                    elif key == 'soil_moisture':
                        data['soil_moisture'] = self._safe_float(value)
                    elif key == 'soil_temp':
                        data['soil_temperature'] = self._safe_float(value)
                    elif key == 'wind_speed':
                        data['wind_speed'] = self._safe_float(value)
                    elif key == 'longitude':
                        data['longitude'] = self._safe_float(value)
                    elif key == 'latitude':
                        data['latitude'] = self._safe_float(value)

            # Check if we have at least a device_id and some sensor data
            if 'device_id' in data and any(key in data for key in ['ambient_temperature', 'humidity', 'soil_moisture', 'soil_temperature', 'wind_speed', 'longitude', 'latitude']):
                data['transmitted'] = False
                return data

        except Exception:
            pass
        return None

    def _parse_generic_format(self, data_string: str) -> Optional[Dict[str, Any]]:
        """Parse generic format by extracting numbers."""
        try:
            # Extract all numbers from the string
            numbers = re.findall(r'-?\d+\.?\d*', data_string)

            if len(numbers) >= 4:
                return {
                    'device_id': 'unknown',
                    'ambient_temperature': self._safe_float(numbers[0]),
                    'humidity': self._safe_float(numbers[1]),
                    'soil_moisture': self._safe_float(numbers[2]),
                    'soil_temperature': self._safe_float(numbers[3]),
                    'wind_speed': self._safe_float(numbers[4]) if len(numbers) > 4 else None,
                    'longitude': self._safe_float(numbers[5]) if len(numbers) > 5 else None,
                    'latitude': self._safe_float(numbers[6]) if len(numbers) > 6 else None,
                    'transmitted': False
                }
        except Exception:
            pass
        return None

    def _safe_float(self, value) -> Optional[float]:
        """Safely convert value to float."""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
