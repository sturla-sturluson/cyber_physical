# use future imports to avoid circular imports
from __future__ import annotations
from src.sensors.mpl_sensor import MplSensor
from ..interfaces import IMagneticSensor




from .ip_helper import get_local_ip
import datetime as dt


def get_ip_string():
    ip_address = get_local_ip()
    return f"Local Ip\n{ip_address}"

def get_current_time_string():
    time_now = dt.datetime.now()
    day_short_string = time_now.strftime("%a")
    day_month_string = time_now.strftime("%d %b")
    hour_min_string = time_now.strftime("%H:%M:%S")
    return f"{day_short_string} {day_month_string}\n{hour_min_string}"

def get_pressure_string(mpl_sensor:MplSensor):
    pressure = mpl_sensor.get_pressure()
    return f"Air Pressure\n{pressure:.2f} Pa"

def get_temperature_string(mpl_sensor:MplSensor):
    temperature = mpl_sensor.get_temperature()
    return f"Temperature\n{temperature:.1f} C°"

def get_altitude_string(mpl_sensor:MplSensor):
    altitude = mpl_sensor.get_altitude()
    return f"Altitude\n{altitude:.1f}m"

def get_compass_string(magnetic_sensor:IMagneticSensor):
    angle,_,nesw = magnetic_sensor.get_data()
    return f"Compass Angle\n{angle:.1f}°\n{nesw}"