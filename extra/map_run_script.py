import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
nSLEEP = 25  # Connect nSLEEP to GPIO 25 or directly to 3.3V/5V
# Set up GPIO pins
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(nSLEEP, GPIO.OUT)
GPIO.output(nSLEEP, GPIO.HIGH)

# Set up PWM on AIN1 and AIN2
pwm_AIN1 = GPIO.PWM(6, 1000)  # 1 kHz frequency
pwm_AIN2 = GPIO.PWM(13, 1000)  # 1 kHz frequency

pwm_AIN1.start(0)
pwm_AIN2.start(0)

pwm_AIN1.ChangeDutyCycle(100)
pwm_AIN2.ChangeDutyCycle(0)
time.sleep(2)

pwm_AIN1.ChangeDutyCycle(0)
pwm_AIN2.ChangeDutyCycle(100)
time.sleep(2)



