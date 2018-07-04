import machine
import time

def blink(sleeptime):
    import machine
    led = machine.Pin(0,machine.Pin.OUT)
    led.value(0)
    time.sleep(sleeptime)
    led.value(1)

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
    blink(.2)
    for i in range(0,5):
        blink(.2)
        time.sleep(3)
        print(i)

    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after 10 seconds (waking the device)
    rtc.alarm(rtc.ALARM0, 3)

    # put the device to sleep
    machine.deepsleep()
