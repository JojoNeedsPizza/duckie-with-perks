from machine import Pin, PWM
import time
import board
import audiopwmio
import audiocore

# PWM-Pins für Motor 1 einrichten (GP8 und GP9)

class wheel_right:
 m1a = PWM(Pin(8)) #backward
 m1b = PWM(Pin(9)) #forward
 buzzer = PWM(Pin(22))

class wheel_left:
    m1a = PWM(Pin(10)) #backward
    m1b = PWM(Pin(11)) #forward
    buzzer = PWM(Pin(22))


# PWM-Frequenz auf 1000 Hz festlegen (Standard für DC-Motoren)
m1a.freq(1000)
m1b.freq(1000)


def motor1_bewegen(geschwindigkeit):
    """
    Steuert Motor 1 mit einer Geschwindigkeit von -100 bis +100 Prozent.
    """
    # Wert auf den Bereich -100 bis 100 begrenzen
    geschwindigkeit = max(-100, min(100, geschwindigkeit))

    # Prozentwert in einen 16-Bit PWM-Wert (0 bis 65535) umrechnen
    pwm_wert = int(abs(geschwindigkeit) / 100 * 65535)

    if geschwindigkeit > 0:
        # Vorwärts drehen
        m1a.duty_u16(pwm_wert)
        m1b.duty_u16(0)
    elif geschwindigkeit < 0:
        # Rückwärts drehen
        m1a.duty_u16(0)
        m1b.duty_u16(pwm_wert)
    else:
        # Motor stoppen
        m1a.duty_u16(0)
        m1b.duty_u16(0)


# --- Testablauf ---
print("Vorwärts mit 70% Geschwindigkeit...")
motor1_bewegen(70)
time.sleep(2)

print("Stopp...")
motor1_bewegen(0)
time.sleep(1)

print("Rückwärts mit 100% Geschwindigkeit...")
motor1_bewegen(-100)
time.sleep(2)

print("Stopp...")
motor1_bewegen(0)


def ton_spielen(frequenz, dauer, lautstaerke=32768):
    """
    Spielt einen Ton mit gegebener Frequenz (Hz) für eine bestimmte Dauer (Sekunden).
    lautstaerke: 0 (aus) bis 65535 (max), 32768 (50%) klingt am saubersten.
    """
    if frequenz > 0:
        buzzer.freq(frequenz)
        buzzer.duty_u16(lautstaerke)
    else:
        # Pause (Frequenz 0)
        buzzer.duty_u16(0)

    time.sleep(dauer)
    buzzer.duty_u16(0)  # Ton am Ende abschalten


# --- Test 1: Einfacher Piepton ---
print("Piep!")
ton_spielen(1000, 0.2)  # 1000 Hz für 0,2 Sekunden
time.sleep(0.5)

# --- Test 2: Kurze Melodie (C-Dur-Dreiklang) ---
noten = [
    (523, 0.2),  # C5
    (659, 0.2),  # E5
    (784, 0.2),  # G5
    (1047, 0.4)  # C6
]

print("Spiele Melodie...")
for freq, zeit in noten:
    ton_spielen(freq, zeit)
    time.sleep(0.05)  # Kurze Trennung zwischen den Tönen

# PWM am Ende sauber deaktivieren
buzzer.deinit()

# afconvert -f WAVE -d UI8@8000 -c 1 dein_sound.mp3 sound.wav


# Piezo-Summer auf Pin GP22 initialisieren
audio = audiopwmio.PWMAudioOut(board.GP22)

# WAV-Datei vom CIRCUITPY-Laufwerk laden
wave_file = open("sound_rp2040.wav", "rb")
wave = audiocore.WaveFile(wave_file)

# Sound einmalig abspielen
audio.play(wave)

# Warten, bis der Sound fertig abgespielt wurde
while audio.playing:
    pass