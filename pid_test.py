from src.motor.pid_reader import PID_READER
from src.constants import A_C1_PIN,A_C2_PIN,B_C1_PIN,B_C2_PIN
import time
import pprint
import os
pp = pprint.PrettyPrinter(indent=4)
def main():
    with  PID_READER(A_C1_PIN,A_C2_PIN) as pid_reader:
        pid_reader.start()
        while True:
            os.system('clear')
            print(pid_reader)
            # for i in range(0,len(pid_reader.angle_arr),10):
            #     pp.pprint(pid_reader.angle_arr[i:i+10])
            time.sleep(0.25)


if __name__ == '__main__':
    main()