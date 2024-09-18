from ..calibrators import RangeSensorCalibrator
import asyncio


def run_range_sensor_calibration():
    calibrator = RangeSensorCalibrator()
    asyncio.run(calibrator.calibrate())
    calibrator.print_results()
    print("Calibration complete.")