from machine import Pin, PWM
import time

buzzer = PWM(Pin(22))

# Dvořák 9 – Largo, „Going Home“-Thema
melodie = [
    (392, 500), (440, 250), (494, 750),
    (440, 500), (392, 250), (330, 750),
    (294, 500), (330, 250), (392, 750),
    (330, 1000),
]

for frequenz, dauer in melodie:
    buzzer.freq(frequenz)
    buzzer.duty_u16(18000)
    time.sleep_ms(dauer)
    buzzer.duty_u16(0)
    time.sleep_ms(60)

buzzer.deinit()