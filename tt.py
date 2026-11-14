from machine import Pin, PWM
import time
import board
import audiopwmio
import audiocore

print("Piep!")
ton_spielen(1000, 0.2)  # 1000 Hz für 0,2 Sekunden
time.sleep(0.5)
