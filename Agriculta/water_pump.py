import RPi.GPIO as GPIO
from time import sleep
import datetime

GPIO.setmode(GPIO.BOARD)
# HIGH = OFF
# LOW = ON
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW) # PUMP
on_time = 1800 # 30 minutes
print("pump on")
now = datetime.datetime.now()
print("{} - PUMP TURNED ON".format(now))
sleep(on_time)
GPIO.output(18, GPIO.HIGH)
print("PUMP ON Finished")
GPIO.cleanup()