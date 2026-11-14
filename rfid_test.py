from machine import UART, Pin
import time

# RFID-TX → GP13
rfid = UART(
    0,
    baudrate=9600,
    tx=Pin(12),
    rx=Pin(13)
)

while True:
    if rfid.any():
        daten = rfid.read()
        print("RFID:", daten)

    time.sleep_ms(50)