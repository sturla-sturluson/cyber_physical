import math
import time

def volt_to_cm(voltage:float):
    return 46.371 * voltage**6 - 462.87 * voltage**5 + 1878.4 * voltage**4 - 3975.3 * voltage**3 + 4655.9 * voltage**2 - 2916.3 * voltage + 828.41



def main():
    voltage = 2.5
    while True:
        voltage -= 0.1
        print("Voltage " + str(voltage))
        print(volt_to_cm(voltage))
        time.sleep(1)



if __name__ == "__main__":
    main()