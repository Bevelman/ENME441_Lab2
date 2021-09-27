import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
p1,p2,p3 = 4,5,6
GPIO.setup(p1, GPIO.OUT)
GPIO.setup(p2, GPIO.OUT)
GPIO.setup(p3, GPIO.OUT)

in1,in2 = 16,20
gpio.setmode(gpio.BCM)
gpio.setup(in1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(in2, gpio.IN, pull_up_down=gpio.PUD_DOWN)

# Define a threaded callback function:
def myCallback(pin):
  print("Rising edge detected on pin %d" % pin)
  if pin==16:
    pwm = GPIO.PWM(p1, 1) # create PWM object @ 100 Hz
    pwm.start(0) # initiate PWM at 0% duty cycle
    for dc in range(101): # loop duty cycle from 0 to 100
      pwm.ChangeDutyCycle(dc) # set duty cycle
      sleep(0.01)             # sleep 10 ms
    for dc in range(101):
      pwm.ChangeDutyCycle(100-dc) # set duty cycle
      sleep(0.01)             # sleep 10 ms
  else:
    pwm = GPIO.PWM(p2, 1) # create PWM object @ 100 Hz
    pwm.start(0) # initiate PWM at 0% duty cycle
    for dc in range(101): # loop duty cycle from 0 to 100
      pwm.ChangeDutyCycle(dc) # set duty cycle
      sleep(0.01)             # sleep 10 ms
    for dc in range(101):
      pwm.ChangeDutyCycle(100-dc) # set duty cycle
      sleep(0.01)             # sleep 10 ms

try:
  # Execute myCallback() if port 1 goes HIGH:
  gpio.add_event_detect(in1, gpio.RISING, callback=myCallback, bouncetime=500)
  # Execute myCallback() if port 2 goes HIGH:
  gpio.add_event_detect(in2, gpio.RISING, callback=myCallback, bouncetime=500)
  while True: # continuous loop
    GPIO.output(p3, 0) # set output to 0V
    sleep(0.5) # wait 0.5 sec
    GPIO.output(p3, 1) # set output to 3.3V
    sleep(0.5)

except KeyboardInterrupt:     # stop gracefully on ctrl-C
  print('\nExiting')

pwm.stop()
GPIO.cleanup()