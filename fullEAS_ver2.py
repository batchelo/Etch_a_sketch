# Display line drawing on I2C driven ssd1306 OLED display 
from machine import Pin, I2C 
import time
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

x_counter = 2
prev_x_counter = 0
y_counter = 2
prev_y_counter = 0
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
    if (x_counter < 1):              #all of this is to limit the counters to the display size
       x_counter = 1
    if (x_counter > 127):
        x_counter = 127
    if (y_counter < 1):
        y_counter = 1
    if (y_counter > 31):
        y_counter = 31
        
    lf_clk_current = lf_clk_pin.value()  #take a read of the current state of the lf clk pin

    if lf_clk_current != lf_clk_previous:  #read the encoder--need to determine direction; 
        if lf_dt_pin.value() != lf_clk_current:  #incement the x_counter on clockwise 
            x_counter = x_counter + 1
            print ("CW--thus x_counter = ", x_counter)
            x_pix = x_counter
            print ("x_pix = ", x_pix)
        else:
            x_counter = x_counter - 1      #decrement the x_counter on counter clockwise
            print ("CCW thus x_counter = ", x_counter)
            x_pix = x_counter
            print ("x_pix = ", x_pix)
        lf_clk_previous = lf_clk_current
        #prev_x_counter = x_counter
        
    rt_clk_current = rt_clk_pin.value()

    if rt_clk_current != rt_clk_previous: #read the encoder--need to determine direction; 
        if rt_dt_pin.value() != rt_clk_current:
            y_counter = y_counter + 1       #incement the y_counter on clockwise
            print ("CW--thus y_counter = ", y_counter)
            y_pix = y_counter
            print ("y_pix = ", y_pix)
        else:
            y_counter = y_counter - 1      #decrement the y_counter on counter clockwise
            print ("CCW--thus y_counter = ", y_counter)
            y_pix = y_counter
            print ("y_pix = ", y_pix)
        rt_clk_previous = rt_clk_current
        
    #display.pixel(x_pix, y_pix, 1)
    #time.sleep_ms(100)
    #display.show()
    
    #display.line(prev_x_pix, prev_y_pix, x_pix, y_pix, 1)
    #time.sleep_ms(50)
    #display.show()
    #if x_counter != prev_x_counter:
        #x_pix = x_counter
        #print ("x_pix = ", x_pix)
    #if y_counter != prev_y_counter:
        #y_pix = y_counter
        #print ("y_pix = ", y_pix)