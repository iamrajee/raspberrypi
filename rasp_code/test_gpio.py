import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
setpin1 = [8]
for pin in setpin1:
  GPIO.setup(pin,GPIO.OUT)

#while True:
 # GPIO.output(pin,True)

m=1.0
count = 10000
const = count/2
while True:
    '''
    if count > const:
        GPIO.output(pin,True)
        count-=1
    elif count == -1:
        count = const*2
    else:
        GPIO.output(pin,False)
        count-=1
    
    #print(count)
    '''
    GPIO.output(pin,True)
    time.sleep(m)
    GPIO.output(pin,False)
    time.sleep(m)
