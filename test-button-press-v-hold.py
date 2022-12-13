# this code will detect a button press vs a button hold and run functions accordingly

import time, math, sys
sys.path.insert(0, 'libraries')
from machine import Pin, SoftI2C
import ssd1306

# define the button - can be any GPIO pin
button = Pin(13, Pin.IN, Pin.PULL_DOWN)

# define the LED - can be any GPIO
led = Pin(14, Pin.OUT, Pin.PULL_DOWN)

# for this one I had the power going from ESP32 to positive rail
# positive rail to button
# button to pin 13
# pin 14 to led (with 100 resistor: brown black black black brown)
# and then both the light and the ESP32 to negative rail


# define the OLED display
i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# start with a blank display and count of 0 and assumption that button is not clicked to start
count = 0.

# let's also make boolean variables for detecting if the button is being clicked or held
buttonIsBeingClicked = False
buttonIsBeingHeld = False
holdThreshhold = .5 # this can change based on what feels right
holdCount = 0.

while True:
    # while True kind of just means 'as long as the program is running'
    
    if button.value():
        # button.value() evaluates to '1' aka 'True' when the button is pressed,
        # or in other words when GPIO pin 13 senses a completed circuit
        # when this is detected, increase count variable value
        count += .1
        # increase based on time interval, so if it's held for .5 seconds it increases by .5
        # print("click count: " + str(round(count, 2)))
        """
        if not buttonIsBeingClicked and not buttonIsBeingHeld:
            print("button is being clicked for the first time, set buttonIsBeingClicked to true")
            buttonIsBeingClicked = True
        """
        if not buttonIsBeingClicked:
            print("click")
            buttonIsBeingClicked = True
            
        if buttonIsBeingClicked and not buttonIsBeingHeld:
            holdCount += .1
            if holdCount > holdThreshhold:
                buttonIsBeingHeld = True
                holdCount = 0.
                print("hold detected")

        
        # wipe display (otherwise it'll write on top)
        display.fill(0)
        # update with the current count value at the upper left corner
        # display.text(str(round(count, 2)), 0, 0, 1)
        display.text("click", 0, 0, 1)
        if buttonIsBeingHeld:
            display.text("HOLD DETECTED", 0, 20, 1)
        display.show()
        
        # turn on light (controlled by GPIO 14- off by default even though the circuit is complete physically)
        led.on()
        
    else:
        # reset click/hold booleans to False, holdCount to 0, clear display
        if buttonIsBeingClicked:
            buttonIsBeingClicked = False
        if buttonIsBeingHeld:
            buttonIsBeingHeld = False
        # wipe display (otherwise it'll write on top)
        display.fill(0)
        display.show()
        holdCount = 0.

        # turn off light whenever button is not pressed
        led.off()
    time.sleep(.1)
    
# thoughts: since holding it will increase it more times it could count duration of being on to a +- .1 second?




