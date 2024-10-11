import RPi.GPIO as GPIO
import sys

def main():
    argc = len(sys.argv)
    list_of_pins = []
    if(argc>1):
        try:
            for i in range(1,argc):
                list_of_pins.append(int(sys.argv[i]))
        except ValueError:
            print(f"Invalid pin number: {sys.argv[i]}")
            return
    # Setting all the pins to LOW
    GPIO.setmode(GPIO.BCM)
    for pin in list_of_pins:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,GPIO.LOW)
    GPIO.cleanup()


main()