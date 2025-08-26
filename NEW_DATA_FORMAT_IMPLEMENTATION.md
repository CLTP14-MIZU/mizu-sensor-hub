# New Sensor Data Format Implementation

## Overview

The MIZU Sensor Hub has been updated to handle a new sensor data format and database schema. This document outlines all the changes made to support the new data format.

## New Data Format

The system now accepts sensor data in the following format:

```
d_id=%s,a_t=%.2f,hum=%.2f,s_m=%.1f,s_t=%.1f,w_s=%.1f,a_l=%.2f,uv_l=%.2f
```

### Field Descriptions

| Field  | Description         | Unit   |
| ------ | ------------------- | ------ |
| `d_id` | Device ID           | String |
| `a_t`  | Ambient Temperature | °C     |
| `hum`  | Humidity            | %      |
| `s_m`  | Soil Moisture       | %      |
| `s_t`  | Soil Temperature    | °C     |
| `w_s`  | Wind Speed          | m/s    |
| `a_l`  | Ambient Light       | lux    |
| `uv_l` | UV Light            | mW/cm² |

## Database Changes

### Schema Updates

1. **Removed Columns:**

   - `longitude` (Float)
   - `latitude` (Float)

2. **Added Columns:**
   - `ambient_light` (Float) - Stores ambient light sensor readings
   - `uv_light` (Float) - Stores UV light sensor readings

### Migration Details

- **Migration File:** `migrations/versions/cb9daef77144_remove_geolocation_add_light_sensors.py`
- **Revision ID:** `cb9daef77144`
- **Previous Revision:** `0002`

## Code Changes

### 1. Database Model Updates (`database_models.py`)

- Updated `SensorData` model to remove longitude/latitude columns
- Added `ambient_light` and `uv_light` columns
- Updated model documentation

### 2. Data Parsing Updates (`database_manager.py`)

- Updated `_parse_key_value_format()` method to handle new field names:

  - `d_id` → `device_id`
  - `a_t` → `ambient_temperature`
  - `hum` → `humidity`
  - `s_m` → `soil_moisture`
  - `s_t` → `soil_temperature`
  - `w_s` → `wind_speed`
  - `a_l` → `ambient_light`
  - `uv_l` → `uv_light`

- Updated all parsing methods to remove longitude/latitude references
- Added support for ambient_light and uv_light in all parsing methods

### 3. UI Display Updates (`mizu_sensor_hub.py`)

- Added `_format_sensor_data_for_display()` method to format sensor data for UI
- Updated `_handle_received_data()` to use formatted display
- Added proper units and labels for all sensor readings:
  - Ambient Temperature: °C
  - Humidity: %
  - Soil Moisture: %
  - Soil Temperature: °C
  - Wind Speed: m/s
  - Ambient Light: lux
  - UV Light: mW/cm²

## UI Display Format

When sensor data is received, it will be displayed in the UI as:

```
=== SENSOR DATA RECEIVED ===
Timestamp: 2025-08-26 16:29:09
Device ID: SENSOR001
Ambient Temperature: 25.50°C
Humidity: 65.20%
Soil Moisture: 45.5%
Soil Temperature: 22.1°C
Wind Speed: 3.2 m/s
Ambient Light: 850.75 lux
UV Light: 2.45 mW/cm²
==============================
```

## Testing

The implementation has been thoroughly tested with:

1. **Data Parsing Tests:** Verified that all sensor data fields are correctly parsed
2. **Database Save Tests:** Confirmed that parsed data is successfully saved to the database
3. **UI Display Tests:** Validated that data is properly formatted for display

## Example Usage

### Sample Data Input

```
d_id=SENSOR001,a_t=25.50,hum=65.20,s_m=45.5,s_t=22.1,w_s=3.2,a_l=850.75,uv_l=2.45
```

### Parsed Output

```python
{
    'device_id': 'SENSOR001',
    'ambient_temperature': 25.5,
    'humidity': 65.2,
    'soil_moisture': 45.5,
    'soil_temperature': 22.1,
    'wind_speed': 3.2,
    'ambient_light': 850.75,
    'uv_light': 2.45,
    'transmitted': False
}
```

## Backward Compatibility

The system maintains backward compatibility with:

- JSON format data
- CSV format data
- Generic number extraction format

However, the new key-value format (`d_id=value,a_t=value,...`) is now the primary supported format.

## Database Migration Status

- ✅ Migration created: `cb9daef77144_remove_geolocation_add_light_sensors.py`
- ✅ Migration applied to database
- ✅ Schema updated successfully
- ✅ New columns added: `ambient_light`, `uv_light`
- ✅ Old columns removed: `longitude`, `latitude`

## Files Modified

1. `database_models.py` - Updated model definition
2. `database_manager.py` - Updated parsing logic
3. `mizu_sensor_hub.py` - Updated UI display logic
4. `migrations/versions/cb9daef77144_remove_geolocation_add_light_sensors.py` - New migration

## Next Steps

1. Test the application with real sensor data
2. Monitor database performance with the new schema
3. Consider adding data validation for sensor value ranges
4. Implement data visualization features for the new sensor types

## Notes

- The system now supports 8 different sensor readings per data transmission
- All sensor data is automatically timestamped when saved to the database
- The UI provides clear, user-friendly display of all sensor readings with appropriate units
- Database operations are fully transactional and include error handling

