# use future imports to avoid circular imports
from __future__ import annotations
from src.sensors.mpl_sensor import MplSensor
from src.sensors.range_sensor import RangeSensor
from src.sensors.rgb_sensor import RgbSensor
from ..interfaces import IMagneticSensor




from .ip_helper import get_local_ip
import datetime as dt


def get_ip_string():
    ip_address = get_local_ip()
    return f"Local Ip\n{ip_address}"

def get_current_date_time_string():
    
    return f"{get_current_date_string()}\n{get_current_time_string()}"

def get_current_date_string():
    time_now = dt.datetime.now()
    day_short_string = time_now.strftime("%a")
    return f"{day_short_string}"

def get_current_time_string():
    time_now = dt.datetime.now()
    hour_min_string = time_now.strftime("%H:%M:%S")
    return f"{hour_min_string}"

def get_pressure_string(mpl_sensor:MplSensor):
    pressure = mpl_sensor.get_pressure()
    return f"Air Pressure\n{pressure:.2f} Pa"

def get_temperature_string(mpl_sensor:MplSensor):
    temperature = mpl_sensor.get_temperature()
    return f"Temperature\n{temperature:.1f} C°"

def get_altitude_string(mpl_sensor:MplSensor):
    altitude = mpl_sensor.get_altitude()
    return f"Altitude\n{altitude:.1f}m"

def get_barometer_string(mpl_sensor:MplSensor):
    pressure = mpl_sensor.get_pressure()
    temperature = mpl_sensor.get_temperature()
    altitude = mpl_sensor.get_altitude()
    return f"Barometer\n{pressure:.2f} hPa\n{temperature:.1f} C°\n{altitude:.1f}m"

def get_compass_string(magnetic_sensor:IMagneticSensor):
    angle,_,nesw = magnetic_sensor.get_data()
    return f"Compass Angle\n{angle:.1f}°\n{nesw}"

def get_range_sensor_string(range_sensor:RangeSensor):
    _,voltage,cm_dist = range_sensor.get_data()
    return f"Range Sensor\n{cm_dist:.2f}cm\n{voltage:.2f}V"
def _def_get_formatted_rgb_number(num:int):
    """
    Returns a formatted string of the number with leading zeros

    """
    if(num < 10):
        return f"  {num}"
    elif(num < 100):
        return f" {num}"
    else:
        return f"{num}"
    #return f"{num:03d}"

def get_color_string(color_sensor:RgbSensor):
    return_str = "RGB Sensor\n"
    r,g,b = color_sensor.get_rgb()
    return_str += f"R:{_def_get_formatted_rgb_number(r)} G:{_def_get_formatted_rgb_number(g)} B:{_def_get_formatted_rgb_number(b)}\n"
    return_str += f"{color_sensor.get_primary_color()}\n"
    return_str += f"{color_sensor.get_color_from_temp()}"
    return return_str
