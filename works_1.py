# Display line drawing on I2C driven ssd1306 OLED display 
from machine import Pin, I2C 
import time
import framebuf
from ssd1306 import SSD1306_I2C

#left rotary encoder (clk=pin2, dt=pin3, sw=pin4)
lf_clk_pin=Pin(2, Pin.IN, Pin.PULL_UP)
lf_dt_pin=Pin(3, Pin.IN, Pin.PULL_UP)
lf_sw_pin=Pin(4, Pin.IN, Pin.PULL_UP)
lf_clk_current = True
lf_clk_previous = lf_clk_pin.value()
lf_dt_current = True
lf_dt_previous = lf_dt_pin.value()
lf_sw_current = True
lf_sw_previous = lf_sw_pin.value()

#right rotary encoder (clk=pin5, dt=pin6, sw=pin7)
rt_clk_pin=Pin(5, Pin.IN, Pin.PULL_UP)
rt_dt_pin=Pin(6, Pin.IN, Pin.PULL_UP)
rt_sw_pin=Pin(7, Pin.IN, Pin.PULL_UP)
rt_clk_current = True
rt_clk_previous = rt_clk_pin.value()
rt_dt_current = True
rt_dt_previous = rt_dt_pin.value()
rt_sw_current = True
rt_sw_previous = rt_sw_pin.value()

x_pix = 0
y_pix = 0
prev_x_pix = 0
prev_y_pix = 0

WIDTH  = 128                                            # oled display width
HEIGHT = 32                                             # oled display height

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display

display.fill(0)        # Clear the oled display.

while True:
    if (x_pix < 1):              #all of this is to limit the counters to the display size
       x_pix = 1
    if (x_pix > 127):
        x_pix = 127
    if (y_pix < 1):
        y_pix = 1
    if (y_pix > 31):
        y_pix = 31
        
    lf_clk_current = lf_clk_pin.value()  #take a read of the current state of the lf clk pin
    if lf_clk_current != lf_clk_previous:  #read the encoder--need to determine direction; 
        if lf_dt_pin.value() != lf_clk_current:  #incement the x_pix on clockwise 
            x_pix = x_pix + 1
            print ("x_pix = ", x_pix)           
            lf_clk_previous = lf_clk_current
            prev_x_pix = x_pix
            display.line(prev_x_pix, prev_y_pix, x_pix, y_pix, 1)
            display.show()
        else:
            x_pix = x_pix - 1      #decrement the x_pix on counter clockwise
            print ("x_pix = ", x_pix)
            lf_clk_previous = lf_clk_current
            prev_x_pix = x_pix
            display.line(prev_x_pix, prev_y_pix, x_pix, y_pix, 1)
            display.show()

    rt_clk_current = rt_clk_pin.value()
    if rt_clk_current != rt_clk_previous: #read the encoder--need to determine direction; 
        if rt_dt_pin.value() != rt_clk_current: #if CW; then
            y_pix = y_pix + 1       #increase the y_pix 
            print ("y_pix = ", y_pix)           
            rt_clk_previous = rt_clk_current
            prev_y_pix = y_pix
            display.line(prev_x_pix, prev_y_pix, x_pix, y_pix, 1)
            display.show()
        else:                                       #if CCW, then
            y_pix = y_pix - 1      #decrease the y_pix by one
            print ("y_pix = ", y_pix)
            rt_clk_previous = rt_clk_current
            prev_y_pix = y_pix
            display.line(prev_x_pix, prev_y_pix, x_pix, y_pix, 1)
            display.show()
