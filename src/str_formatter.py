from .ip_helper import get_local_ip
import datetime as dt
from .mpl_sensor import Mpl_Sensor

def get_ip_string():
    ip_address = get_local_ip()
    return f"Local Ip\n{ip_address}"

def get_current_time_string():
    time_now = dt.datetime.now()
    day_short_string = time_now.strftime("%a")
    day_month_string = time_now.strftime("%d %b")
    hour_min_string = time_now.strftime("%H:%M:%S")
    return f"{day_short_string} {day_month_string}\n{hour_min_string}"

def get_pressure_string(mpl_sensor:Mpl_Sensor):
    pressure = mpl_sensor.get_pressure()
    return f"Air Pressure\n{pressure:.2f} Pa"

def get_temperature_string(mpl_sensor:Mpl_Sensor):
    temperature = mpl_sensor.get_temperature()
    return f"Temperature\n{temperature:.1f} C°"

def get_altitude_string(mpl_sensor:Mpl_Sensor):
    altitude = mpl_sensor.get_altitude()
    return f"Altitude\n{altitude:.1f}m"
