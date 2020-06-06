import threading
import time
import sys
#import Adafruit_DHT
import Adafruit_DHT  # Comment if not using temp sensor
from adafruit_crickit import crickit


from time import sleep, strftime
import RPi.GPIO as GPIO

GPIO.cleanup()
motor_2 = crickit.dc_motor_2  # Init motor 2 on HAT
  

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

# Get and print temp/humidity data, Comment if not using temp sensor   
def temp_loop():
    """Get and print temp/humidity data """
    humidity, temperature = Adafruit_DHT.read_retry(11, 17)  # Read DHT11 temp/humidity data from pin17
    if humidity is not None and temperature is not None:
        print('Humidity: ' + str(humidity) + '  Temp: ' + str(temperature *9/5 + 32) )   # display the time
    else:
        print("Could not read")
    sleep(1)
    
# Flash LED t times    
def flashLed(count):
    """flash the specified led .25s - on, .25s - off """
    print("My LED")
    for i in range(count):
        GPIO.output(21, True)
        time.sleep(0.25)
        GPIO.output(21, False)
        time.sleep(0.25)
        
def destroy():
    GPIO.cleanup()
    

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        while True:
            #temp_loop()
            if crickit.touch_1.value:
                print("Touched Cap Touch Pad 1")
                motor_2.throttle = -1 # full speed backward
                time.sleep(1)
                motor_2.throttle = 1 # full speed backward
                time.sleep(1)
                motor_2.throttle = 0 # full speed backward
                time.sleep(1)
            if crickit.touch_2.value:
                print("Touched Cap Touch Pad 2")
                temp_loop()   # Comment if not using temp sensor
            if crickit.touch_3.value:
                print("Touched Cap Touch Pad 3")
                print("Moving servo #1")
                crickit.servo_1.angle = 0      # right
                time.sleep(1)
                crickit.servo_1.angle = 90     # middle
                time.sleep(1)
                crickit.servo_1.angle = 180    # left
                time.sleep(1)
                crickit.servo_1.angle = 90     # middle
                time.sleep(1)
            if crickit.touch_4.value:
                print("Touched Cap Touch Pad 4")
                # Use thread so rest of program keeps running during blinking
                t = threading.Thread(target=flashLed(3))
                t.start()
                time.sleep(0.5)  # Wait .5s so we don't sense double touch
    except KeyboardInterrupt:
        destroy()