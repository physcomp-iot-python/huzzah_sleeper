import board
import digitalio
import machine
import time
import sys
from analogio import AnalogIn
import gc

import adafruit_io

SLEEP_SECONDS=3

# Network 'Hotspot' settings
ESSID    = 'dolphnet'
PASSWORD = 'mcmlxix1969'

#-Adafruit IO settings
USER_NAME = "donblair" #PLEASE CHANGE TO YOUR AIO USERNAME
AIO_KEY = '3515b3ecee734780927d7f4ab1654917'  #PLEASE CHANGE TO YOUR AIO KEY

# create one adafruit_io.Feed object per sensor, configure once during
# instantiation, and use to post values many times.
# Each sensor's' feed should have a unique name!

ANALOG_FEED_NAME = 'analog-feed-test-number-1' #PLEASE CHANGE TO YOUR AIO FEED NAME
analog_feed = adafruit_io.Feed(user_name = USER_NAME,
                               key = AIO_KEY,
                               feed_name = ANALOG_FEED_NAME,
                               )
print("Feed: {}".format(ANALOG_FEED_NAME))
print("headers: {}".format(analog_feed.headers))
print("post_url: {}".format(analog_feed.post_url))

# some utility functions
def get_adc():
    with AnalogIn(board.ADC) as ai:
        return ai.value/65535.0
    
def blink(sleeptime):
    import machine
    led = machine.Pin(0,machine.Pin.OUT)
    led.value(0)
    time.sleep(sleeptime)
    led.value(1)

def do_connect(essid=ESSID,password=PASSWORD):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(essid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
def go_to_sleep(seconds):
    
    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after 10 seconds (waking the device)
    rtc.alarm(rtc.ALARM0, seconds)

    blink(1)
    # put the device to sleep
    machine.deepsleep()


while True:
    
    do_connect() #connect to network


    try:
        adc_value = get_adc()
        print("adc: %0.3f" % adc_value)
        analog_feed.post(adc_value)
        blink(0.5)
        #time.sleep(10)
        gc.collect()
        blink(.2)
        
        for i in range(0,5):
            blink(.2)
            time.sleep(3)
            print(i)

        # configure RTC.ALARM0 to be able to wake the device
        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

        # set RTC.ALARM0 to fire after X seconds (waking the device)
        rtc.alarm(rtc.ALARM0, 3)

        # put the device to sleep
        machine.deepsleep()
    except KeyboardInterrupt:
        # this is needed for ampy and other REPL interactions to work with this
        # generic error handler
        raise KeyboardInterrupt
    except Exception as exc:
        print("Caught: {}".format(repr(exc)))
        blink(0.5)
        time.sleep(10)
        gc.collect()
        
    

