from ..calibrators  import CompassCalibrator
import asyncio

def run_compass_calibration():
    # compass_calibrator = CompassCalibrator(FakeMagneticSensor())
    compass_calibrator = CompassCalibrator()
    asyncio.run(compass_calibrator.calibrate())


