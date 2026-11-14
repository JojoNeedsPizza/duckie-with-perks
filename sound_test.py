from machine import Pin, PWM
import time

buzzer = PWM(Pin(22))

def ton(frequenz, dauer, lautstaerke=18000):
    buzzer.freq(frequenz)
    buzzer.duty_u16(lautstaerke)
    time.sleep_ms(dauer)
    buzzer.duty_u16(0)
    time.sleep_ms(25)

def silly_playful_sound():
    # "Ta-da!"
    ton(523, 100)
    ton(659, 100)
    ton(784, 180)

    # hüpfender Quietscher
    for frequenz in (900, 600, 1000, 500, 1200):
        ton(frequenz, 70)

    # lustiges Plopp
    for frequenz in range(700, 120, -40):
        ton(frequenz, 15, 14000)

    ton(180, 300, 22000)

silly_playful_sound()
buzzer.deinit()