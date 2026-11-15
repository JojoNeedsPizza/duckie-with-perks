from machine import Pin, PWM
import time
import struct

# Piezo-Summer auf GP22 einrichten
buzzer = PWM(Pin(22))
buzzer.freq(62500)  # Hohe Trägerfrequenz für sauberen PWM-Ton
buzzer.duty_u16(0)

def play_wav(filename):
    with open(filename, "rb") as f:
        # WAV-Header (erste 44 Bytes) überspringen
        f.seek(44)
        while True:
            data = f.read(1024)
            if not data:
                break
            # 16-Bit Samples (LEI16) auslesen
            for i in range(0, len(data) - 1, 2):
                sample = struct.unpack_from("<h", data, i)[0]
                buzzer.duty_u16(sample + 32768)
                time.sleep_us(40)  # Timing für 16 kHz Abtastrate
    buzzer.duty_u16(0)

play_wav("../Sounds/sound.wav")
