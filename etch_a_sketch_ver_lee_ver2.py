# Display line drawing on I2C driven ssd1306 OLED display 
from machine import Pin, I2C, 
import time
from ssd1306 import SSD1306_I2C

#left rotary encoder (clk=pin2, dt=pin3, sw=pin4)
lf_clk_pin=Pin(2, Pin.IN, Pin.PULL_UP)
lf_dt_pin=Pin(3, Pin.IN, Pin.PULL_UP)
lf_sw_pin=Pin(4, Pin.IN, Pin.PULL_UP)
lf_previousValue = True

#right rotary encoder (clk=pin5, dt=pin6, sw=pin7)
rt_clk_pin=Pin(5, Pin.IN, Pin.PULL_UP)
rt_dt_pin=Pin(6, Pin.IN, Pin.PULL_UP)
rt_sw_pin=Pin(7, Pin.IN, Pin.PULL_UP)
rt_previousValue = True

x_counter = 0
y_counter = 0
x_pix = 64
y_pix = 32
prev_x_pix = 0
prev_y_pix = 0

WIDTH  = 128                                            # oled display width
HEIGHT = 32                                             # oled display height

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display

display.fill(0)        # Clear the oled display.

while True:
    if (x_counter < 1):              #all of this is to limit the counters to the display size
       x_counter = 1
    if (x_counter > 127):
        x_counter = 127
    if (y_counter < 1):
        y_counter = 1
    if (y_counter > 31):
        y_counter = 31

    if lf_previousValue != lf_dt_pin.value():  #read the encoder--need to determine direction; 
        if lf_dt_pin.value() == False:         #incement the x_counter on clockwise 
            if lf_clk_pin.value() == False:    
                x_counter = x_counter + 1
                print (x_counter, "x clockwise")
            else:
                x_counter = x_counter - 1      #decrement the x_counter on counter clockwise
                print (x_counter, "x counter clockwise")
        lf_previousValue = lf_dt_pin.value() 

    if rt_previousValue != rt_dt_pin.value():  #read the encoder--need to determine direction; 
        if rt_dt_pin.value() == False:
            if rt_clk_pin.value() == False:
               y_counter = y_counter + 1       #incement the y_counter on clockwise
               print (y_counter, "y clockwise")
            else:
                y_counter = y_counter - 1      #decrement the y_counter on counter clockwise
                print (y_counter, "y counter clockwise")
        rt_previousValue = rt_dt_pin.value()

    x_pix = x_counter                #needed just because I wanted to test the counter
    y_pix = y_counter                #value and the pixel value separately   

    display.line(prev_x_pix, prev_y_pix, x_pix, y_pix, 1)
    time.sleep_ms(50)
    display.show()

    prev_x_pix = x_pix
    prev_y_pix = y_pix