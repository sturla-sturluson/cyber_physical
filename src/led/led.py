try:
    import RPi.GPIO as GPIO
except RuntimeError:
    #from src.utils import mock_gpio as GPIO
    ...

class Led:
    LED_PIN:int
    IS_ON:bool = False

    def __init__(self, led_pin:int): 
        self.LED_PIN = led_pin
        if(GPIO.getmode() == None):
            print("Setting GPIO mode")
            GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        self.turn_off()

    def toggle(self):
        if self.IS_ON:
            self.turn_off()
        else:
            self.turn_on()

    def turn_on(self):
        if(not self.IS_ON):
            self.IS_ON = True
            GPIO.output(self.LED_PIN, GPIO.HIGH)

    def turn_off(self):
        if(self.IS_ON):
            self.IS_ON = False
            GPIO.output(self.LED_PIN, GPIO.LOW)

    def cleanup(self):
        GPIO.output(self.LED_PIN, GPIO.LOW)
        GPIO.cleanup()