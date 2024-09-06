import RPi.GPIO as GPIO

class Led:
    LED_PIN:int
    IS_ON:bool = False

    def __init__(self, led_pin:int): 
        self.LED_PIN = led_pin
        if(GPIO.getmode() == None):
            print("Setting GPIO mode")
            GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.LED_PIN, GPIO.OUT)

        # Start with LED ON
        self.turn_on()

    def toggle(self):
        self.IS_ON = not self.IS_ON
        if self.IS_ON:
            self.turn_on()
        else:
            self.turn_off()
        print(f"LED is {'ON' if self.IS_ON else 'OFF'}")

    def turn_on(self):
        GPIO.output(self.LED_PIN, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.LED_PIN, GPIO.LOW)

    def cleanup(self):
        GPIO.output(self.LED_PIN, GPIO.LOW)
        GPIO.cleanup()