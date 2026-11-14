from machine import Pin, PWM
import time

buzzer = PWM(Pin(22))

def ton(frequenz, dauer):
    buzzer.freq(frequenz)
    buzzer.duty_u16(18000)
    time.sleep_ms(dauer)
    buzzer.duty_u16(0)
    time.sleep_ms(40)

def silly_sound():
    ton(300, 150)
    ton(600, 150)
    ton(250, 300)
    ton(800, 100)
    ton(180, 400)
    ton(1000, 80)
    ton(120, 500)

silly_sound()
buzzer.deinit()