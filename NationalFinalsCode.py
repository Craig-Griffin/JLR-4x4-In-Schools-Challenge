#THE DOCS
#National Finals Code

import RPi.GPIO as GPIO
import time, math
import lcddriver
display = lcddriver.lcd()


#Configuring Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#Electrical Connections

a_pin = 18 #LDR Charge Output
b_pin = 23 #LDR Charge Input
GPIO.setup(20, GPIO.OUT)#Buzzer
GPIO.setup(17, GPIO.OUT)#Front white leds
GPIO.setup(8, GPIO.OUT) #Yellow Right Indicator
GPIO.setup(25, GPIO.OUT)#Yellow Left Indicator
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button 1 -- Increasing Light Value
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button 2 -- Decreasing Light Value
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Tilt Sensor 1
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Tilt Sensor 2


#Base Light Level 
x = 25


#Discharging Capacitor 
def discharge():
    GPIO.setup(a_pin, GPIO.IN)
    GPIO.setup(b_pin, GPIO.OUT)
    GPIO.output(b_pin, False)
    time.sleep(0.01)

# return the time taken for the voltage on the capacitor to to activate the pin
def charge_time():
    GPIO.setup(b_pin, GPIO.IN)
    GPIO.setup(a_pin, GPIO.OUT)
    GPIO.output(a_pin, True)
    t1 = time.time()
    while not GPIO.input(b_pin):
        pass
    t2 = time.time()
    return (t2 - t1) * 1000000

#Combining the 2 functions 
def analog_read():
    discharge()
    return charge_time()

# Convert the time taken to charge the cpacitor into a value of resistance
def read_resistance():
    n = 20 #Change the accuracy with this
    total = 0;
    for i in range(1, n):
        total = total + analog_read()
    reading = total / float(n)
    resistance = reading * 5 - 939 #These are the values that have been used to convert the resistance into an "approximate" lux value
    return resistance

def light_from_r(R):
    # Log the reading to compress the range so that the LDR does not return lots of different values
    return math.log(1000000.0/R) * 10.0 -30

#taking the values from the above functions to 
def Light():
    Light =  light_from_r(read_resistance())
    reading_str = "{:.0f}".format(Light) 
    display.lcd_display_string("Light Level:" + reading_str, 2)
    return int(reading_str)

#The Logic
while True:
    print Light()
    Button1_state = GPIO.input(12)
    Button2_state = GPIO.input(16)
    tilt_state = GPIO.input(22)
    tilt_state2 = GPIO.input(27)
    GPIO.output(25, GPIO.LOW) # Turning the LEDS to Low for the Indicator Effect
    GPIO.output(8, GPIO.LOW)
#light operational control
    if Button1_state == False:
        x=x+1

        print "operational light level" +str(x)
        display.lcd_clear()
        display.lcd_display_string (">", 2)
 if Button2_state == False:
        x=x-1
        display.lcd_clear()
        display.lcd_display_string ("<", 2)
        print "operational light level " + str(x)

    if Light() < x:
        print "Lights: ON"
        GPIO.output(17, GPIO.HIGH) 
        GPIO.output(8, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
        display.lcd_clear()
        display.lcd_display_string ("IPIG", 1)
        time.sleep(0.01)

    elif tilt_state == False:
        display.lcd_clear()
        display.lcd_display_string("TILT WARNING!", 1)
        GPIO.output(25, GPIO.HIGH)
        GPIO.output(8, GPIO.LOW)
        GPIO.output(20, GPIO.HIGH)

    elif tilt_state2 == False:
        display.lcd_clear()
        display.lcd_display_string("TILT WARNING!", 1)
        GPIO.output(8, GPIO.HIGH)
        GPIO.output(25, GPIO.LOW)
        GPIO.output(20, GPIO.HIGH)

    else:
        print "BRIGHT WORKS"
        GPIO.output(8, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(20, GPIO.LOW)
        display.lcd_clear()
        display.lcd_display_string("BrightWorks", 1)
        time.sleep(0.01)

GPIO.Cleanup()






