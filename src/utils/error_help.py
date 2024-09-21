import os
import datetime as dt

def save_error_report(error_report:str) -> None:
    """Saves the error report to a file and prints the error"""
    timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"error_report_{timestamp}.txt","w") as f:
        f.write(error_report)
    print(error_report)