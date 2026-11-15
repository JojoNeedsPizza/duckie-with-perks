from machine import Pin, PWM
import time

taste = Pin(17, Pin.IN, Pin.PULL_UP)
buzzer = PWM(Pin(22))

def quak():
    for frequenz, dauer in ((180, 120), (100, 180), (160, 100)):
        buzzer.freq(frequenz)
        buzzer.duty_u16(20000)
        time.sleep_ms(dauer)
        buzzer.duty_u16(0)
        time.sleep_ms(20)

while True:
    if taste.value() == 0:
        quak()
        while taste.value() == 0:
            time.sleep_ms(20)

    time.sleep_ms(20)